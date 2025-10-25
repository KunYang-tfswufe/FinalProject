# Saffron_Edge_Server/app.py (优化版 v2)

import serial
import json
import threading
import time
import io, csv
from datetime import datetime
from flask import Flask, jsonify, render_template, request, Response
from flask_cors import CORS
import os
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash

# --- 修改点 1：将摄像头相关代码移到全局 ---
PI_CAMERA_AVAILABLE = False
picam2 = None # 全局摄像头对象
try:
    from picamera2 import Picamera2
    # 仅创建实例，不在这里启动
    picam2 = Picamera2()
    PI_CAMERA_AVAILABLE = True
    print("✅ picamera2 库加载成功，摄像头对象已创建。")
except Exception as e:
    print(f"⚠️ 警告: picamera2 初始化失败: {e}。拍照功能将不可用。")
# --- 结束修改 ---


# 数据库集成
try:
    from . import db as db
except Exception:
    import db

# --- 全局变量 (未改变) ---
data_lock = threading.Lock()
latest_data = { "temperature": None, "humidity": None, "lux": None, "soil": None, "timestamp": None }
db.create_tables()
DB_DEVICE_ID = db.ensure_default_device()
serial_lock = threading.Lock()
SECRET_KEY = os.environ.get('SECRET_KEY', 'saffron-secret')
TOKEN_MAX_AGE = int(os.environ.get('TOKEN_MAX_AGE', str(7*24*3600)))
serializer = URLSafeTimedSerializer(SECRET_KEY, salt='auth-token')
REQUIRE_ADMIN_FOR_CONTROL = os.environ.get('REQUIRE_ADMIN_FOR_CONTROL', '0') in ('1','true','TRUE')
ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN', 'saffron-admin')
ser = None
auto_irrigation_state = { "watering": False, "last_start_ts": None, "last_end_ts": None }

# 摄像头照片保存目录
CAPTURES_DIR = os.path.join(os.path.dirname(__file__), 'static', 'captures')
if not os.path.exists(CAPTURES_DIR):
    os.makedirs(CAPTURES_DIR)

# --- 原有的函数 (此处省略未修改的代码以保持简洁) ---
def _get_bearer_token():
    auth = request.headers.get('Authorization', '')
    if auth.startswith('Bearer '): return auth[len('Bearer '):].strip()
    return None
def issue_token(user_id: int) -> str: return serializer.dumps({'uid': int(user_id)})
def verify_token(token: str):
    try:
        data = serializer.loads(token, max_age=TOKEN_MAX_AGE)
        return int(data.get('uid'))
    except (BadSignature, SignatureExpired, Exception): return None
def get_current_user():
    token = _get_bearer_token()
    if not token: return None
    uid = verify_token(token)
    if not uid: return None
    user = db.get_user_by_id(uid)
    if not user: return None
    user['roles'] = db.get_user_roles(uid)
    return user
def auth_required(fn):
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user: return jsonify({"error": "unauthorized"}), 401
        request.current_user = user
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper
def admin_required(fn):
    def wrapper(*args, **kwargs):
        provided = request.headers.get('X-Admin-Token')
        if provided == ADMIN_TOKEN: return fn(*args, **kwargs)
        user = get_current_user()
        if not user or ('admin' not in (user.get('roles') or [])): return jsonify({"error": "admin required"}), 403
        request.current_user = user
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper
def serial_reader():
    """后台线程，负责读取串口数据并更新 latest_data。"""
    global latest_data, ser
    serial_port = '/dev/ttyACM0'
    baud_rate = 115200
    while True:
        try:
            with serial_lock:
                ser = serial.Serial(serial_port, baud_rate, timeout=2)
            print(f"后台线程: 成功连接到串口 {serial_port}")
            while True:
                line = ser.readline()
                if line:
                    try:
                        decoded_line = line.decode('utf-8').strip()
                        if 'temp' in decoded_line:
                            data = json.loads(decoded_line)
                            ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                            with data_lock:
                                latest_data['temperature'] = data.get('temp')
                                latest_data['humidity'] = data.get('humi')
                                latest_data['lux'] = data.get('lux')
                                latest_data['soil'] = data.get('soil')
                                latest_data['timestamp'] = ts
                            try:
                                db.insert_sensor_data(DB_DEVICE_ID, data.get('temp'), data.get('humi'), data.get('lux'), data.get('soil'), ts)
                                db.update_device_last_seen(DB_DEVICE_ID)
                            except Exception: pass
                    except (UnicodeDecodeError, json.JSONDecodeError, KeyError): pass
        except serial.SerialException as e:
            print(f"后台线程: 串口错误 - {e}. 5秒后重试...")
            time.sleep(5)
def irrigation_worker():
    global ser
    POLL_INTERVAL = 5
    while True:
        try:
            policy = db.get_irrigation_policy(DB_DEVICE_ID)
            if not policy or not policy.get('enabled'):
                time.sleep(POLL_INTERVAL); continue
            threshold = policy.get('soil_threshold_min')
            duration = policy.get('watering_seconds')
            cooldown = policy.get('cooldown_seconds') or 0
            if threshold is None or duration is None or duration <= 0:
                time.sleep(POLL_INTERVAL); continue
            try: cd = int(cooldown)
            except Exception: cd = 0
            if cd > 0 and auto_irrigation_state.get("last_end_ts"):
                try:
                    last_end = datetime.strptime(auto_irrigation_state["last_end_ts"], '%Y-%m-%d %H:%M:%S')
                    if (datetime.utcnow() - last_end).total_seconds() < cd:
                        time.sleep(POLL_INTERVAL); continue
                except Exception: pass
            with data_lock: soil = latest_data.get('soil')
            if soil is None:
                time.sleep(POLL_INTERVAL); continue
            if soil < threshold and not auto_irrigation_state["watering"]:
                cmd_on = json.dumps({"actuator": "pump", "action": "on"})
                success_on = False
                with serial_lock:
                    if ser and ser.is_open:
                        try:
                            ser.write((cmd_on + "\n").encode('utf-8')); success_on = True
                        except Exception: success_on = False
                try: db.insert_control_log(DB_DEVICE_ID, "pump", "on", cmd_on, success_on)
                except Exception: pass
                if success_on:
                    auto_irrigation_state["watering"] = True
                    auto_irrigation_state["last_start_ts"] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                    time.sleep(int(duration))
                    cmd_off = json.dumps({"actuator": "pump", "action": "off"})
                    success_off = False
                    with serial_lock:
                        if ser and ser.is_open:
                            try:
                                ser.write((cmd_off + "\n").encode('utf-8')); success_off = True
                            except Exception: success_off = False
                    try: db.insert_control_log(DB_DEVICE_ID, "pump", "off", cmd_off, success_off)
                    except Exception: pass
                    if success_off: auto_irrigation_state["last_end_ts"] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                    auto_irrigation_state["watering"] = False
            time.sleep(POLL_INTERVAL)
        except Exception: time.sleep(POLL_INTERVAL)
# --- 结束省略 ---

app = Flask(__name__)
CORS(app)

# --- 路由 (此处省略大部分未修改的路由) ---
@app.route('/')
def index(): return render_template('index.html')
# ... 其他页面路由 ...
@app.route('/admin')
def admin_page(): return render_template('admin.html')
@app.route('/history')
def history_page(): return render_template('history.html')
@app.route('/login')
def login_page(): return render_template('login.html')

# --- 修改点 2：简化拍照API端点 ---
@app.route('/api/v1/camera/capture', methods=['POST'])
def capture_photo():
    """处理拍照请求，使用全局摄像头对象。"""
    if not PI_CAMERA_AVAILABLE or not picam2:
        return jsonify({"status": "error", "message": "摄像头模块不可用或未初始化。"}), 503

    try:
        # 1. 定义文件名和路径
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"saffron_{timestamp}.jpg"
        filepath = os.path.join(CAPTURES_DIR, filename)
        
        # 2. 直接拍照并保存 (不再需要 start/stop)
        picam2.capture_file(filepath)
        print(f"照片已保存至: {filepath}")
        
        # 3. 返回成功响应
        relative_path = os.path.join('static', 'captures', filename)
        return jsonify({
            "status": "success", 
            "message": f"照片拍摄成功！",
            "path": relative_path
        })
            
    except Exception as e:
        print(f"❌ 拍照失败: {e}")
        return jsonify({"status": "error", "message": f"拍照失败: {e}"}), 500
# --- 结束修改 ---

# --- 其他未修改的 API 路由 (省略) ---
@app.route('/api/v1/control', methods=['POST'])
def control_device():
    # ... 省略 ...
    if REQUIRE_ADMIN_FOR_CONTROL:
        provided = request.headers.get('X-Admin-Token')
        user = get_current_user()
        roles = (user.get('roles') if user else []) or []
        if not (provided == ADMIN_TOKEN or ('admin' in roles)): return jsonify({"error":"admin required"}), 403
    data = request.get_json()
    command = data.get('command')
    if not command: return jsonify({"status": "error", "message": "Command not provided"}), 400
    success = False
    actuator = None
    action = None
    try:
        parsed = json.loads(command)
        actuator = parsed.get('actuator')
        action = parsed.get('action')
    except Exception: pass
    with serial_lock:
        if ser and ser.is_open:
            try:
                ser.write((command + '\n').encode('utf-8'))
                success = True
            except Exception as e: print(f"串口写入错误: {e}")
    try:
        db.insert_control_log(DB_DEVICE_ID, actuator, action, command, success)
        if success: db.update_device_last_seen(DB_DEVICE_ID)
    except Exception: pass
    if success: return jsonify({"status": "success", "message": f"Command '{command}' sent."})
    else: return jsonify({"status": "error", "message": "Device not connected or busy."}), 503
# ... 省略其他API路由 ...
@app.route('/api/v1/auth/register', methods=['POST'])
def register():
    payload = request.get_json(silent=True) or {}
    username = (payload.get('username') or '').strip()
    password = payload.get('password') or ''
    if not username or not password: return jsonify({"error":"username/password required"}), 400
    if db.get_user_by_username(username): return jsonify({"error":"username exists"}), 409
    pwd_hash = generate_password_hash(password)
    uid = db.create_user(username, pwd_hash)
    try:
        if db.count_users() == 1: db.assign_role_to_user(uid, 'admin')
    except Exception: pass
    token = issue_token(uid)
    return jsonify({"id": uid, "username": username, "roles": db.get_user_roles(uid), "token": token})
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    payload = request.get_json(silent=True) or {}
    username = (payload.get('username') or '').strip()
    password = payload.get('password') or ''
    user = db.get_user_by_username(username)
    if not user or not check_password_hash(user['password_hash'], password): return jsonify({"error":"invalid credentials"}), 401
    token = issue_token(user['id'])
    return jsonify({"token": token, "id": user['id'], "username": user['username'], "roles": db.get_user_roles(user['id'])})
@app.route('/api/v1/auth/me', methods=['GET'])
@auth_required
def me():
    u = request.current_user
    return jsonify({"id": u['id'], "username": u['username'], "roles": u.get('roles', [])})
@app.route('/api/v1/sensors/latest', methods=['GET'])
def get_latest_sensor_data():
    with data_lock: data_to_return = latest_data.copy()
    return jsonify(data_to_return)
@app.route('/api/v1/sensors/history', methods=['GET'])
def get_sensor_history():
    def normalize_start_end(s: str | None, e: str | None):
        def norm_one(x: str | None, is_start: bool):
            if not x: return None
            x = x.strip()
            if len(x) == 10 and x[4] == '-' and x[7] == '-': return x + (' 00:00:00' if is_start else ' 23:59:59')
            return x
        return norm_one(s, True), norm_one(e, False)
    start, end = normalize_start_end(request.args.get('start'), request.args.get('end'))
    try:
        limit = max(1, min(1000, int(request.args.get('limit', '100'))))
        offset = max(0, int(request.args.get('offset', '0')))
    except Exception: return jsonify({"error": "invalid limit/offset"}), 400
    try: device_id = int(request.args.get('device_id')) if request.args.get('device_id') is not None else DB_DEVICE_ID
    except Exception: return jsonify({"error": "invalid device_id"}), 400
    rows = db.query_sensor_history(device_id=device_id, start=start, end=end, limit=limit, offset=offset)
    return jsonify({"items": rows, "count": len(rows)})
@app.route('/api/v1/policy/irrigation', methods=['GET'])
def get_irrigation_policy_api():
    try: device_id = int(request.args.get('device_id')) if request.args.get('device_id') is not None else DB_DEVICE_ID
    except Exception: return jsonify({"error": "invalid device_id"}), 400
    row = db.get_irrigation_policy(device_id)
    return jsonify(row or {})
@app.route('/api/v1/policy/irrigation', methods=['POST'])
def set_irrigation_policy_api():
    payload = request.get_json(silent=True) or {}
    provided = request.headers.get('X-Admin-Token') or payload.get('admin_token') or request.args.get('admin_token')
    is_admin = False
    user = get_current_user()
    if user and ('admin' in (user.get('roles') or [])): is_admin = True
    elif provided == ADMIN_TOKEN: is_admin = True
    if not is_admin: return jsonify({"error": "admin required"}), 403
    enabled = payload.get('enabled')
    if enabled in (True, False): enabled_int = 1 if enabled else 0
    elif isinstance(enabled, int) and enabled in (0, 1): enabled_int = enabled
    else: return jsonify({"error": "enabled must be boolean"}), 400
    try:
        soil_v = float(payload.get('soil_threshold_min')) if payload.get('soil_threshold_min') is not None else None
        dur_v = int(payload.get('watering_seconds')) if payload.get('watering_seconds') is not None else None
        cd_v = int(payload.get('cooldown_seconds')) if payload.get('cooldown_seconds') is not None else None
    except Exception: return jsonify({"error": "invalid soil_threshold_min/watering_seconds/cooldown_seconds"}), 400
    try: device_id = int(payload.get('device_id')) if payload.get('device_id') is not None else DB_DEVICE_ID
    except Exception: return jsonify({"error": "invalid device_id"}), 400
    db.upsert_irrigation_policy(device_id, enabled_int, soil_v, dur_v, cd_v)
    row = db.get_irrigation_policy(device_id)
    return jsonify(row or {}), 200
@app.route('/api/v1/policy/irrigation/status', methods=['GET'])
def get_auto_irrigation_status(): return jsonify(auto_irrigation_state)
@app.route('/api/v1/sensors/history.csv', methods=['GET'])
def get_sensor_history_csv():
    def normalize_start_end(s: str | None, e: str | None):
        def norm_one(x: str | None, is_start: bool):
            if not x: return None
            x = x.strip()
            if len(x) == 10 and x[4] == '-' and x[7] == '-': return x + (' 00:00:00' if is_start else ' 23:59:59')
            return x
        return norm_one(s, True), norm_one(e, False)
    start, end = normalize_start_end(request.args.get('start'), request.args.get('end'))
    try:
        limit = max(1, min(10000, int(request.args.get('limit', '1000'))))
        offset = max(0, int(request.args.get('offset', '0')))
    except Exception: return jsonify({"error": "invalid limit/offset"}), 400
    try: device_id = int(request.args.get('device_id')) if request.args.get('device_id') is not None else DB_DEVICE_ID
    except Exception: return jsonify({"error": "invalid device_id"}), 400
    rows = db.query_sensor_history(device_id=device_id, start=start, end=end, limit=limit, offset=offset)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['id','device_id','timestamp','temperature','humidity','lux','soil'])
    for r in rows: writer.writerow([r.get('id'), r.get('device_id'), r.get('timestamp'), r.get('temperature'), r.get('humidity'), r.get('lux'), r.get('soil')])
    csv_data = output.getvalue()
    return Response(csv_data, mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename="history.csv"'})
@app.route('/api/v1/control/logs', methods=['GET'])
def get_control_logs():
    try:
        limit = max(1, min(1000, int(request.args.get('limit', '100'))))
        offset = max(0, int(request.args.get('offset', '0')))
    except Exception: return jsonify({"error": "invalid limit/offset"}), 400
    try: device_id = int(request.args.get('device_id')) if request.args.get('device_id') is not None else DB_DEVICE_ID
    except Exception: return jsonify({"error": "invalid device_id"}), 400
    actuator = request.args.get('actuator')
    def norm(ts, is_start):
        if not ts: return None
        ts = ts.strip()
        if len(ts) == 10 and ts[4] == '-' and ts[7] == '-': return ts + (' 00:00:00' if is_start else ' 23:59:59')
        return ts
    start = norm(request.args.get('start'), True)
    end = norm(request.args.get('end'), False)
    rows = db.query_control_logs_range(device_id=device_id, start=start, end=end, actuator=actuator, limit=limit, offset=offset)
    return jsonify({"items": rows, "count": len(rows)})
@app.route('/api/v1/devices/status', methods=['GET'])
def device_status():
    try: device_id = int(request.args.get('device_id')) if request.args.get('device_id') is not None else DB_DEVICE_ID
    except Exception: return jsonify({"error": "invalid device_id"}), 400
    row = db.query_device_status(device_id)
    if not row: return jsonify({"error": "device not found"}), 404
    return jsonify(row)


if __name__ == '__main__':
    # --- 修改点 3：在主程序启动时，真正启动摄像头 ---
    if PI_CAMERA_AVAILABLE and picam2:
        try:
            # 这里的 still_config 只是一个例子，你可以根据需要配置
            # 对于简单拍照，默认配置通常就足够了
            still_config = picam2.create_still_configuration()
            picam2.configure(still_config)
            picam2.start()
            print("✅ 摄像头已成功启动并准备就绪。")
        except Exception as e:
            print(f"❌ 启动摄像头失败: {e}")
            PI_CAMERA_AVAILABLE = False # 如果启动失败，就标记为不可用
    # --- 结束修改 ---

    reader_thread = threading.Thread(target=serial_reader, daemon=True)
    reader_thread.start()

    irrigation_thread = threading.Thread(target=irrigation_worker, daemon=True)
    irrigation_thread.start()

    print("启动统一服务器... 请在浏览器中访问 http://<你的树莓派IP>:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)

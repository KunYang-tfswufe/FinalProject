import serial
import json
import threading
import time
import io, csv
from datetime import datetime
from flask import Flask, jsonify, render_template, request, Response # 增加 request
from flask_cors import CORS
import os


# 数据库集成
try:
    # Prefer package-style import when available
    from . import db as db
except Exception:
    import db  # fallback when running as a script

# --- 全局变量 ---
data_lock = threading.Lock()
latest_data = {
    "temperature": None,
    "humidity": None,
    "lux": None,
    "soil": None,
    "timestamp": None
}

# 初始化数据库和默认设备
db.create_tables()
DB_DEVICE_ID = db.ensure_default_device()

# --- 新增：全局共享的串口对象和锁 ---
# 这个锁将保护对 ser 对象的访问，确保读写操作不会冲突
serial_lock = threading.Lock()
# 简易管理员口令（可通过环境变量 ADMIN_TOKEN 覆盖）
ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN', 'saffron-admin')

ser = None # 将串口对象设为全局，以便API路由可以访问


# --- 自动灌溉状态（内存） ---
auto_irrigation_state = {
    "watering": False,
    "last_start_ts": None,
    "last_end_ts": None
}

# --- 串口读取线程函数 (稍作修改以使用全局 ser) ---
def serial_reader():
    """后台线程，负责读取串口数据并更新 latest_data。"""
    global latest_data, ser
    serial_port = '/dev/ttyACM0'
    baud_rate = 115200

    while True:
        try:
            # 尝试连接，并将连接对象赋给全局变量
            with serial_lock:
                ser = serial.Serial(serial_port, baud_rate, timeout=2)
            print(f"后台线程: 成功连接到串口 {serial_port}")

            while True:
                line = ser.readline()
                if line:
                    try:
                        decoded_line = line.decode('utf-8').strip()
                        # 忽略STM32的响应消息，只处理传感器数据包
                        if 'temp' in decoded_line:
                            data = json.loads(decoded_line)
                            ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                            with data_lock:
                                latest_data['temperature'] = data.get('temp')
                                latest_data['humidity'] = data.get('humi')
                                latest_data['lux'] = data.get('lux')
                                latest_data['soil'] = data.get('soil')
                                latest_data['timestamp'] = ts
                            # Persist to DB and update last_seen
                            try:
                                db.insert_sensor_data(DB_DEVICE_ID, data.get('temp'), data.get('humi'), data.get('lux'), data.get('soil'), ts)
                                db.update_device_last_seen(DB_DEVICE_ID)
                            except Exception:
                                pass
                        # else:
                            # 可以在这里打印或记录STM32的响应, e.g., print(f"STM32 Response: {decoded_line}")
                    except (UnicodeDecodeError, json.JSONDecodeError, KeyError):
                        pass # 静默处理不规范的数据行

        except serial.SerialException as e:
            print(f"后台线程: 串口错误 - {e}. 5秒后重试...")

# --- 自动灌溉后台线程 ---

def irrigation_worker():
    """后台线程：根据 irrigation_policies 自动控制水泵开/关。
    策略：若 enabled 且 soil < soil_threshold_min，则打开水泵 watering_seconds 秒后关闭。
    """
    global ser
    POLL_INTERVAL = 5  # 秒
    while True:
        try:
            policy = db.get_irrigation_policy(DB_DEVICE_ID)
            if not policy or not policy.get('enabled'):
                time.sleep(POLL_INTERVAL)
                continue

            threshold = policy.get('soil_threshold_min')
            duration = policy.get('watering_seconds')
            cooldown = policy.get('cooldown_seconds') or 0
            if threshold is None or duration is None or duration <= 0:
                time.sleep(POLL_INTERVAL)
                continue
            # Respect cooldown since last end
            try:
                cd = int(cooldown)
            except Exception:
                cd = 0
            if cd > 0 and auto_irrigation_state.get("last_end_ts"):
                try:
                    last_end = datetime.strptime(auto_irrigation_state["last_end_ts"], '%Y-%m-%d %H:%M:%S')
                    if (datetime.utcnow() - last_end).total_seconds() < cd:
                        time.sleep(POLL_INTERVAL)
                        continue
                except Exception:
                    pass

            # 读取当前土壤湿度
            with data_lock:
                soil = latest_data.get('soil')
            if soil is None:
                time.sleep(POLL_INTERVAL)
                continue

            # 若满足条件且当前未在浇水
            if soil < threshold and not auto_irrigation_state["watering"]:
                # 发送开泵指令
                cmd_on = json.dumps({"actuator": "pump", "action": "on"})
                success_on = False
                with serial_lock:
                    if ser and ser.is_open:
                        try:
                            ser.write((cmd_on + "\n").encode('utf-8'))
                            success_on = True
                        except Exception:
                            success_on = False
                # 记录日志
                try:
                    db.insert_control_log(DB_DEVICE_ID, "pump", "on", cmd_on, success_on)
                except Exception:
                    pass

                if success_on:
                    auto_irrigation_state["watering"] = True
                    auto_irrigation_state["last_start_ts"] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                    # 持续浇水指定秒数
                    time.sleep(int(duration))
                    # 发送关泵指令
                    cmd_off = json.dumps({"actuator": "pump", "action": "off"})
                    success_off = False
                    with serial_lock:
                        if ser and ser.is_open:
                            try:
                                ser.write((cmd_off + "\n").encode('utf-8'))
                                success_off = True
                            except Exception:
                                success_off = False
                    try:
                        db.insert_control_log(DB_DEVICE_ID, "pump", "off", cmd_off, success_off)
                    except Exception:
                        pass
                    if success_off:
                        auto_irrigation_state["last_end_ts"] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                    auto_irrigation_state["watering"] = False

            time.sleep(POLL_INTERVAL)
        except Exception:
            # 任意异常，避免线程崩溃
            time.sleep(POLL_INTERVAL)


# --- Flask Web应用 ---
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/history')
def history_page():
    return render_template('history.html')

@app.route('/api/v1/sensors/latest', methods=['GET'])
def get_latest_sensor_data():
    with data_lock:
        data_to_return = latest_data.copy()
    return jsonify(data_to_return)

# --- 新增：控制API端点 ---
@app.route('/api/v1/control', methods=['POST'])
def control_device():
    """接收前端的控制命令，并通过串口发送给STM32。"""
    # 从POST请求的JSON体中获取命令
    data = request.get_json()
    command = data.get('command')

    if not command:
        return jsonify({"status": "error", "message": "Command not provided"}), 400

    success = False
    # 尝试解析结构化命令以便记录日志
    actuator = None
    action = None
    try:
        parsed = json.loads(command)
        actuator = parsed.get('actuator')
        action = parsed.get('action')
    except Exception:
        pass

    with serial_lock: # 获取串口锁
        if ser and ser.is_open:
            try:
                # 命令需要以换行符结尾，因为STM32端使用 readline()
                ser.write((command + '\n').encode('utf-8'))
                success = True
            except Exception as e:
                print(f"串口写入错误: {e}")

    # 写入控制日志
    try:
        db.insert_control_log(DB_DEVICE_ID, actuator, action, command, success)
        if success:
            db.update_device_last_seen(DB_DEVICE_ID)
    except Exception:
        pass

    if success:
        return jsonify({"status": "success", "message": f"Command '{command}' sent."})
    else:
        # Service Unavailable
        return jsonify({"status": "error", "message": "Device not connected or busy."}), 503

# --- 历史数据查询 API ---
@app.route('/api/v1/sensors/history', methods=['GET'])
def get_sensor_history():
    def normalize_start_end(s: str | None, e: str | None):
        def norm_one(x: str | None, is_start: bool):
            if not x:
                return None
            x = x.strip()
            if len(x) == 10 and x[4] == '-' and x[7] == '-':
                return x + (' 00:00:00' if is_start else ' 23:59:59')
            return x
        return norm_one(s, True), norm_one(e, False)

    start = request.args.get('start')
    end = request.args.get('end')
    start, end = normalize_start_end(start, end)

    try:
        limit = max(1, min(1000, int(request.args.get('limit', '100'))))
        offset = max(0, int(request.args.get('offset', '0')))
    except Exception:
        return jsonify({"error": "invalid limit/offset"}), 400

# --- 灌溉策略 API ---
@app.route('/api/v1/policy/irrigation', methods=['GET'])
def get_irrigation_policy_api():
    device_id = request.args.get('device_id')
    try:
        device_id = int(device_id) if device_id is not None else DB_DEVICE_ID
    except Exception:
        return jsonify({"error": "invalid device_id"}), 400
    row = db.get_irrigation_policy(device_id)
    return jsonify(row or {})


@app.route('/api/v1/policy/irrigation', methods=['POST'])
def set_irrigation_policy_api():
    payload = request.get_json(silent=True) or {}

    # 简易管理员认证：Header X-Admin-Token 或 JSON/admin_token 或 QueryString
    provided = request.headers.get('X-Admin-Token') or payload.get('admin_token') or request.args.get('admin_token')
    if provided != ADMIN_TOKEN:
        return jsonify({"error": "unauthorized"}), 401

    enabled = payload.get('enabled')
    soil_threshold_min = payload.get('soil_threshold_min')
    watering_seconds = payload.get('watering_seconds')
    cooldown_seconds = payload.get('cooldown_seconds')

    # basic validation
    if enabled in (True, False):
        enabled_int = 1 if enabled else 0
    elif isinstance(enabled, int) and enabled in (0, 1):
        enabled_int = enabled
    else:
        return jsonify({"error": "enabled must be boolean"}), 400

    try:
        soil_v = float(soil_threshold_min) if soil_threshold_min is not None else None
        dur_v = int(watering_seconds) if watering_seconds is not None else None
        cd_v = int(cooldown_seconds) if cooldown_seconds is not None else None
    except Exception:
        return jsonify({"error": "invalid soil_threshold_min/watering_seconds/cooldown_seconds"}), 400

    device_id = payload.get('device_id')
    try:
        device_id = int(device_id) if device_id is not None else DB_DEVICE_ID
    except Exception:
        return jsonify({"error": "invalid device_id"}), 400

    db.upsert_irrigation_policy(device_id, enabled_int, soil_v, dur_v, cd_v)
    row = db.get_irrigation_policy(device_id)
    return jsonify(row or {}), 200


@app.route('/api/v1/policy/irrigation/status', methods=['GET'])
def get_auto_irrigation_status():
    return jsonify({
        "watering": auto_irrigation_state["watering"],
        "last_start_ts": auto_irrigation_state["last_start_ts"],
        "last_end_ts": auto_irrigation_state["last_end_ts"]
    })



# --- 历史数据 CSV 导出 API ---
@app.route('/api/v1/sensors/history.csv', methods=['GET'])
def get_sensor_history_csv():
    def normalize_start_end(s: str | None, e: str | None):
        def norm_one(x: str | None, is_start: bool):
            if not x:
                return None
            x = x.strip()
            if len(x) == 10 and x[4] == '-' and x[7] == '-':
                return x + (' 00:00:00' if is_start else ' 23:59:59')
            return x
        return norm_one(s, True), norm_one(e, False)

    start = request.args.get('start')
    end = request.args.get('end')
    start, end = normalize_start_end(start, end)

    try:
        limit = max(1, min(10000, int(request.args.get('limit', '1000'))))
        offset = max(0, int(request.args.get('offset', '0')))
    except Exception:
        return jsonify({"error": "invalid limit/offset"}), 400

    device_id = request.args.get('device_id')
    try:
        device_id = int(device_id) if device_id is not None else DB_DEVICE_ID
    except Exception:
        return jsonify({"error": "invalid device_id"}), 400

    rows = db.query_sensor_history(device_id=device_id, start=start, end=end,
                                   limit=limit, offset=offset)
    # Build CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['id','device_id','timestamp','temperature','humidity','lux','soil'])
    for r in rows:
        writer.writerow([r.get('id'), r.get('device_id'), r.get('timestamp'),
                         r.get('temperature'), r.get('humidity'), r.get('lux'), r.get('soil')])
    csv_data = output.getvalue()
    return Response(csv_data, mimetype='text/csv', headers={
        'Content-Disposition': 'attachment; filename="history.csv"'
    })



# --- 控制日志查询 API ---
@app.route('/api/v1/control/logs', methods=['GET'])
def get_control_logs():
    try:
        limit = max(1, min(1000, int(request.args.get('limit', '100'))))
        offset = max(0, int(request.args.get('offset', '0')))
    except Exception:
        return jsonify({"error": "invalid limit/offset"}), 400

    device_id = request.args.get('device_id')
    try:
        device_id = int(device_id) if device_id is not None else DB_DEVICE_ID
    except Exception:
        return jsonify({"error": "invalid device_id"}), 400

    # optional filters
    actuator = request.args.get('actuator')
    start = request.args.get('start')
    end = request.args.get('end')
    # allow YYYY-MM-DD shortcuts
    def norm(ts, is_start):
        if not ts:
            return None
        ts = ts.strip()
        if len(ts) == 10 and ts[4] == '-' and ts[7] == '-':
            return ts + (' 00:00:00' if is_start else ' 23:59:59')
        return ts
    start = norm(start, True)
    end = norm(end, False)

    rows = db.query_control_logs_range(device_id=device_id, start=start, end=end,
                                       actuator=actuator, limit=limit, offset=offset)
    return jsonify({"items": rows, "count": len(rows)})


# --- 程序主入口 (代码未改变) ---

# --- 设备状态查询 API ---
@app.route('/api/v1/devices/status', methods=['GET'])
def device_status():
    device_id = request.args.get('device_id')
    try:
        device_id = int(device_id) if device_id is not None else DB_DEVICE_ID
    except Exception:
        return jsonify({"error": "invalid device_id"}), 400
    row = db.query_device_status(device_id)
    if not row:
        return jsonify({"error": "device not found"}), 404
    return jsonify(row)

if __name__ == '__main__':
    reader_thread = threading.Thread(target=serial_reader, daemon=True)
    reader_thread.start()

    irrigation_thread = threading.Thread(target=irrigation_worker, daemon=True)
    irrigation_thread.start()

    print("启动统一服务器... 请在浏览器中访问 http://<你的树莓派IP>:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)

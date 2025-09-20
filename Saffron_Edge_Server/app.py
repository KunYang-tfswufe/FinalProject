import serial
import json
import threading
import time
import io, csv
from datetime import datetime
from flask import Flask, jsonify, render_template, request, Response # 增加 request
from flask_cors import CORS

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
ser = None # 将串口对象设为全局，以便API路由可以访问

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
        finally:
            with serial_lock:
                if ser and ser.is_open:
                    ser.close()
                ser = None # 断开连接后，重置全局变量
            time.sleep(5)

# --- Flask Web应用 ---
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

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

    device_id = request.args.get('device_id')
    try:
        device_id = int(device_id) if device_id is not None else DB_DEVICE_ID
    except Exception:
        return jsonify({"error": "invalid device_id"}), 400

    rows = db.query_sensor_history(device_id=device_id, start=start, end=end,
                                   limit=limit, offset=offset)
    return jsonify({"items": rows, "count": len(rows)})

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

    rows = db.query_control_logs(device_id=device_id, limit=limit, offset=offset)
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
    print("启动统一服务器... 请在浏览器中访问 http://<你的树莓派IP>:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)

import serial
import json
import threading
import time
from flask import Flask, jsonify
from flask_cors import CORS  # <--- 1. 导入CORS

# --- 全局变量 ---
# 使用线程锁来确保线程安全
data_lock = threading.Lock()
# 用一个字典来存储最新的传感器数据
latest_data = {
    "temperature": None,
    "humidity": None,
    "timestamp": None
}

# --- 串口读取线程 ---
def serial_reader():
    """在后台线程中持续读取串口数据并更新全局变量。"""
    global latest_data
    serial_port = '/dev/ttyACM0'
    baud_rate = 115200
    
    while True:
        ser = None
        try:
            ser = serial.Serial(serial_port, baud_rate, timeout=2)
            print(f"后台线程: 串口 {serial_port} 连接成功。")
            
            while True:
                line = ser.readline()
                if line:
                    try:
                        decoded_line = line.decode('utf-8').strip()
                        data = json.loads(decoded_line)
                        
                        # 获取线程锁，安全地更新全局数据
                        with data_lock:
                            latest_data['temperature'] = data.get('temp')
                            latest_data['humidity'] = data.get('humi')
                            latest_data['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
                        
                        print(f"数据更新: {latest_data}")

                    except (UnicodeDecodeError, json.JSONDecodeError, KeyError) as e:
                        print(f"后台线程: 数据处理错误 - {e}")
        
        except serial.SerialException as e:
            print(f"后台线程: 串口错误 - {e}")
            print("后台线程: 5秒后重试...")
            time.sleep(5) # 如果串口连接失败，等待5秒后重试
        finally:
            if ser and ser.is_open:
                ser.close()
                print("后台线程: 串口已关闭。")

# --- Flask Web 应用 ---
app = Flask(__name__)
CORS(app)  # <--- 2. 启用CORS，允许所有来源的跨域请求

@app.route('/api/v1/sensors/latest', methods=['GET'])
def get_latest_sensor_data():
    """API端点，返回最新的传感器数据。"""
    # 获取线程锁，安全地读取全局数据
    with data_lock:
        # 创建一个数据的副本以避免竞态条件
        data_to_return = latest_data.copy()
    
    return jsonify(data_to_return)

if __name__ == '__main__':
    # 创建并启动后台串口读取线程
    # 设置为守护线程(daemon=True)，这样主线程退出时它也会跟着退出
    reader_thread = threading.Thread(target=serial_reader, daemon=True)
    reader_thread.start()
    
    # 启动 Flask 开发服务器
    # host='0.0.0.0' 使其可以被局域网中的其他设备访问
    print("启动 Flask API 服务器... 请访问 http://<你的树莓派IP>:5000/api/v1/sensors/latest")
    app.run(host='0.0.0.0', port=5000, debug=False) # debug=False 在生产中更稳定

import serial
import json
import threading
import time
from flask import Flask, jsonify, render_template
from flask_cors import CORS

# --- 全局变量 ---
# 使用线程锁来确保对共享数据访问的线程安全
data_lock = threading.Lock()
# 用一个字典来存储从STM32接收到的最新传感器数据
latest_data = {
    "temperature": None,
    "humidity": None,
    "timestamp": None
}

# --- 串口读取线程函数 ---
def serial_reader():
    """
    这个函数在一个独立的后台线程中运行，负责：
    1. 持续尝试连接并读取串口数据。
    2. 解析收到的JSON字符串。
    3. 线程安全地更新全局变量latest_data。
    4. 处理串口错误和数据解析错误，并能自动重连。
    """
    global latest_data
    serial_port = '/dev/ttyACM0'
    baud_rate = 115200
    
    while True:
        ser = None
        try:
            # 尝试初始化并打开串口
            ser = serial.Serial(serial_port, baud_rate, timeout=2)
            print(f"后台线程: 成功连接到串口 {serial_port}")
            
            # 成功连接后，进入内层循环持续读取
            while True:
                line = ser.readline()
                if line:
                    try:
                        # 将收到的字节解码为UTF-8字符串，并去除首尾的空白符（如\r\n）
                        decoded_line = line.decode('utf-8').strip()
                        data = json.loads(decoded_line)
                        
                        # 获取线程锁，以保证数据更新操作的原子性，防止多线程冲突
                        with data_lock:
                            latest_data['temperature'] = data.get('temp')
                            latest_data['humidity'] = data.get('humi')
                            latest_data['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
                        
                    except (UnicodeDecodeError, json.JSONDecodeError, KeyError) as e:
                        # 捕获并打印解码、JSON解析或键值错误，但程序不中断
                        print(f"后台线程: 数据处理错误 - {e}, 原始数据: {line}")
        
        except serial.SerialException as e:
            # 捕获串口相关的错误（如设备未找到、权限问题等）
            print(f"后台线程: 串口错误 - {e}")
            print("后台线程: 5秒后将自动重试...")
            time.sleep(5) # 等待5秒后，外层while循环会再次尝试连接串口
        finally:
            # 确保无论发生什么情况，串口连接最终都会被关闭
            if ser and ser.is_open:
                ser.close()
                print("后台线程: 串口已关闭。")

# --- Flask Web应用 ---
# 初始化Flask应用
app = Flask(__name__)
# 为Flask应用启用CORS支持，允许跨域请求。
# 虽然现在网页和API同源了，但保留它对未来开发和调试有益。
CORS(app)

# 新增的路由规则: 定义根URL('/')的行为
@app.route('/')
def index():
    """当用户访问网站主页时，此函数被调用。"""
    # render_template会去'templates'文件夹中寻找并渲染指定的HTML文件
    return render_template('index.html')

# API路由规则: 定义数据接口URL的行为
@app.route('/api/v1/sensors/latest', methods=['GET'])
def get_latest_sensor_data():
    """当JS前端请求最新数据时，此函数被调用。"""
    # 同样使用线程锁来安全地读取全局变量
    with data_lock:
        # 创建一个数据的副本再返回，这是一个好的编程习惯
        data_to_return = latest_data.copy()
    
    # 将Python字典转换为JSON格式的HTTP响应
    return jsonify(data_to_return)

# --- 程序主入口 ---
if __name__ == '__main__':
    # 创建一个线程来运行serial_reader函数
    # 设置为守护线程(daemon=True)，这样当主程序（Flask服务）退出时，该线程也会自动结束
    reader_thread = threading.Thread(target=serial_reader, daemon=True)
    reader_thread.start()
    
    # 启动Flask的开发服务器
    # host='0.0.0.0'让服务器监听所有网络接口，使其可以被局域网内的其他设备访问
    # port=5000 指定服务运行的端口号
    print("启动统一服务器... 请在浏览器中访问 http://<你的树莓派IP>:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)

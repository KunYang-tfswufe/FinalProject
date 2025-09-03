import serial
import time
import json

# --- 配置区 ---
# 确认 NUCLEO 板在树莓派上的设备名是这个
serial_port = '/dev/ttyACM0' 
baud_rate = 115200
# --------------

def main():
    """主函数，用于连接串口并持续读取数据。"""
    print(f"尝试连接串口: {serial_port}，波特率: {baud_rate}")
    
    ser = None
    try:
        ser = serial.Serial(serial_port, baud_rate, timeout=2)
        print("串口连接成功！等待数据...")
        
        while True:
            line = ser.readline()
            
            if line:
                try:
                    decoded_line = line.decode('utf-8').strip()
                    print(f"收到原始字符串: {decoded_line}")
                    
                    data = json.loads(decoded_line)
                    print(f"解析JSON成功: 温度={data['temp']}, 湿度={data['humi']}")
                    print("-" * 20)
                    
                except (UnicodeDecodeError, json.JSONDecodeError, KeyError) as e:
                    print(f"数据处理错误: {e}, 原始数据: {line}")
                    
            else:
                print("等待数据超时...")

    except serial.SerialException as e:
        print(f"串口错误: {e}")
    except KeyboardInterrupt:
        print("\n程序被用户中断。正在关闭...")
    finally:
        if ser and ser.is_open:
            ser.close()
            print("串口已关闭。")

if __name__ == '__main__':
    main()

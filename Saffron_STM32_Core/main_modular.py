# 藏红花培育系统主程序 - 模块化版本 v7.1 (增加反向控制)
# 集成温湿度、光照、土壤湿度传感器，并能接收控制指令

import machine
import time
import json
import sys
import select # 导入select模块用于非阻塞串口监听

# --- 导入驱动 (代码未改变) ---
try:
    from drivers import create_dht11_sensor, get_driver_info
    class BH1750:
        def __init__(self, i2c, addr=0x23):
            self.i2c = i2c
            self.addr = addr
            self.is_initialized = False
            try:
                self.i2c.writeto(self.addr, b'\x01') # Power On
                time.sleep_ms(10)
                self.i2c.writeto(self.addr, b'\x10') # Continuous High Res Mode
                time.sleep_ms(120)
                self.is_initialized = True
                print("✅ 光照传感器(BH1750)初始化成功")
            except Exception as e:
                print(f"❌ 光照传感器初始化失败: {e}. 请检查I2C连接，地址是否为{hex(self.addr)}")

        def read_lux(self):
            if not self.is_initialized:
                return None
            try:
                data = self.i2c.readfrom(self.addr, 2)
                raw = (data[0] << 8) | data[1]
                return raw / 1.2
            except Exception as e:
                return None
                
    print("✅ 所有驱动模块加载成功")

except ImportError as e:
    print(f"❌ 关键驱动模块导入失败: {e}, 系统无法启动。")
    sys.exit()

print("\n=== 藏红花培育系统 v7.1 - 多传感器与反向控制 ===")

# --- 硬件初始化 (代码未改变) ---
try:
    status_led = machine.Pin('C13', machine.Pin.OUT)
    status_led.high()
    print("✅ 系统LED初始化成功")
except Exception as e:
    status_led = None

try:
    print("\n[1/3] 初始化 DHT11 温湿度传感器...")
    sensor_pin = machine.Pin('A1', machine.Pin.IN, machine.Pin.PULL_UP)
    dht11 = create_dht11_sensor(sensor_pin, 'DHT11')
    print(f"✅ DHT11 初始化成功 (驱动模式: {dht11.driver_mode})")
except Exception as e:
    print(f"❌ DHT11 初始化失败: {e}")
    dht11 = None

try:
    print("\n[2/3] 初始化 BH1750 光照传感器...")
    i2c = machine.I2C(1, freq=100000)
    devices = i2c.scan()
    if not devices:
        print("   - 警告: I2C总线上未发现任何设备！")
    else:
        print(f"   - I2C扫描发现设备: {[hex(d) for d in devices]}")
    light_sensor = BH1750(i2c)
except Exception as e:
    print(f"❌ I2C或光照传感器初始化失败: {e}")
    light_sensor = None

try:
    print("\n[3/3] 初始化土壤湿度传感器...")
    soil_adc = machine.ADC(machine.Pin('A2'))
    print("✅ 土壤湿度传感器初始化成功")
except Exception as e:
    print(f"❌ 土壤湿度传感器初始化失败: {e}")
    soil_adc = None

# --- 新增功能：命令处理器 ---
def process_command(cmd):
    """解析并执行从树莓派传来的命令"""
    cmd = cmd.strip() # 去除换行符
    if cmd == "led_on":
        if status_led:
            status_led.low() # low是点亮
        print('{"response": "LED is ON"}') # 向树莓派反馈
    elif cmd == "led_off":
        if status_led:
            status_led.high() # high是熄灭
        print('{"response": "LED is OFF"}') # 向树莓派反馈
    # 在这里可以扩展更多命令, 如 "pump_on", "pump_off" 等
    else:
        print('{"error": "Unknown command"}')


# --- 主循环 ---
print("\n🚀 开始多传感器数据采集与命令监听循环...")
print("-" * 50)
cycle_count = 0

# 创建一个poll对象来监听标准输入(串口)
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

while True:
    # --- 新增功能：检查并处理控制指令 ---
    # 检查串口是否有数据传入，超时设为0 (非阻塞)
    poll_results = poll_obj.poll(0)
    if poll_results:
        command = sys.stdin.readline()
        process_command(command)

    # --- 传感器数据采集 (这部分逻辑保持不变) ---
    cycle_count += 1
    data_packet = {
        "temp": None, "humi": None, "lux": None, "soil": None,
        "cycle": cycle_count, "timestamp": time.ticks_ms()
    }

    if dht11 and dht11.measure():
        sensor_data = dht11.get_data()
        if sensor_data.get('is_valid'):
            data_packet['temp'] = sensor_data.get('temperature')
            data_packet['humi'] = sensor_data.get('humidity')

    if light_sensor:
        lux_val = light_sensor.read_lux()
        if lux_val is not None:
             data_packet['lux'] = round(lux_val, 1)

    if soil_adc:
        try:
            raw_value = soil_adc.read_u16()
            DRY_VALUE, WET_VALUE = 59000, 26000
            if WET_VALUE <= raw_value <= DRY_VALUE + 2000:
                percentage = 100 * (DRY_VALUE - raw_value) / (DRY_VALUE - WET_VALUE)
                data_packet['soil'] = round(max(0, min(100, percentage)))
        except Exception:
            pass
            
    # --- 数据发送 (逻辑保持不变) ---
    json_string = json.dumps(data_packet)
    print(json_string)
    
    # 指示灯逻辑调整：不再短闪，由命令控制
    # 原有的短闪代码被移除

    # 每3秒重复一次循环
    time.sleep(3)

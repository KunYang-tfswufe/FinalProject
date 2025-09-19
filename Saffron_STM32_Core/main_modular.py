# 藏红花培育系统主程序 - 模块化版本 v7.2 (非阻塞优化)
# 实现即时命令响应和定时传感器读取

import machine
import time
import json
import sys
import select

# --- 导入驱动 (代码未改变) ---
try:
    from drivers import create_dht11_sensor, get_driver_info
    class BH1750:
        def __init__(self, i2c, addr=0x23):
            self.i2c = i2c
            self.addr = addr
            self.is_initialized = False
            try:
                self.i2c.writeto(self.addr, b'\x01')
                time.sleep_ms(10)
                self.i2c.writeto(self.addr, b'\x10')
                time.sleep_ms(120)
                self.is_initialized = True
            except Exception as e:
                print(f"❌ BH1750 初始化失败: {e}")
        def read_lux(self):
            if not self.is_initialized: return None
            try:
                data = self.i2c.readfrom(self.addr, 2)
                return ((data[0] << 8) | data[1]) / 1.2
            except: return None
    print("✅ 所有驱动模块加载成功")
except ImportError as e:
    print(f"❌ 关键驱动模块导入失败: {e}"); sys.exit()

print("\n=== 藏红花培育系统 v7.2 - 高响应非阻塞模式 ===")

# --- 硬件初始化 (代码未改变) ---
status_led = machine.Pin('C13', machine.Pin.OUT, value=1)
dht11 = None
light_sensor = None
soil_adc = None

try: dht11 = create_dht11_sensor(machine.Pin('A1', machine.Pin.IN, machine.Pin.PULL_UP), 'DHT11')
except Exception as e: print(f"❌ DHT11 初始化失败: {e}")

try:
    i2c = machine.I2C(1, freq=100000)
    light_sensor = BH1750(i2c)
except Exception as e: print(f"❌ 光照传感器初始化失败: {e}")

try: soil_adc = machine.ADC(machine.Pin('A2'))
except Exception as e: print(f"❌ 土壤湿度传感器初始化失败: {e}")

# --- 命令处理器 (代码未改变) ---
def process_command(cmd):
    cmd = cmd.strip()
    if cmd == "led_on":
        status_led.low()
        print('{"response": "LED is ON"}')
    elif cmd == "led_off":
        status_led.high()
        print('{"response": "LED is OFF"}')
    else:
        print('{"error": "Unknown command"}')

# --- 主循环 (核心修改) ---
print("\n🚀 开始非阻塞数据采集与命令监听循环...")
print("-" * 50)
cycle_count = 0

# --- 新增：任务调度相关的变量 ---
# 定义传感器读取的时间间隔 (单位：毫秒)
# 这个值决定了数据上报的频率，可以自由调整
SENSOR_READ_INTERVAL = 1000  # <<-- 这里从3秒缩短到1秒
last_sensor_read_time = time.ticks_ms()

poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

# --- 主循环现在将尽可能快地运行 ---
while True:
    # 任务1: 检查并处理控制指令 (每次循环都做，所以响应极快)
    if poll_obj.poll(0):
        command = sys.stdin.readline()
        process_command(command)

    # 任务2: 检查是否到了读取传感器的时间
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_sensor_read_time) >= SENSOR_READ_INTERVAL:
        last_sensor_read_time = current_time  # 重置计时器

        # --- 以下是传感器数据采集和发送的代码，与之前相同 ---
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
            if lux_val is not None: data_packet['lux'] = round(lux_val, 1)

        if soil_adc:
            try:
                raw_value = soil_adc.read_u16()
                DRY_VALUE, WET_VALUE = 59000, 26000
                if WET_VALUE <= raw_value <= DRY_VALUE + 2000:
                    percentage = 100 * (DRY_VALUE - raw_value) / (DRY_VALUE - WET_VALUE)
                    data_packet['soil'] = round(max(0, min(100, percentage)))
            except: pass
                
        json_string = json.dumps(data_packet)
        print(json_string)
        
    # 不再有大的 time.sleep()。循环会快速重复，让系统保持“清醒”
    # 可以加一个非常小的延时，防止CPU 100% 占用，但通常不是必须的
    # time.sleep_ms(10)

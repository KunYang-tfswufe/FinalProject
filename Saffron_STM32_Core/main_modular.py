# 藏红花培育系统主程序 - 模块化版本 v7.4 (修正继电器逻辑)
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

print("\n=== 藏红花培育系统 v7.4 - 高响应非阻塞模式 ===")

# --- 硬件初始化 ---
status_led = machine.Pin('C13', machine.Pin.OUT, value=1)
dht11 = None
light_sensor = None
soil_adc = None
pump_relay = None # 初始化水泵变量
led_strip_relay = None # 初始化LED灯带变量

try: dht11 = create_dht11_sensor(machine.Pin('A1', machine.Pin.IN, machine.Pin.PULL_UP), 'DHT11')
except Exception as e: print(f"❌ DHT11 初始化失败: {e}")

try:
    i2c = machine.I2C(1, freq=100000)
    light_sensor = BH1750(i2c)
except Exception as e: print(f"❌ 光照传感器初始化失败: {e}")

try: soil_adc = machine.ADC(machine.Pin('A2'))
except Exception as e: print(f"❌ 土壤湿度传感器初始化失败: {e}")

# --- 修正：初始化水泵继电器引脚 (B10) 为高电平触发逻辑 ---
try:
    # 对于高电平触发模块：
    # 初始值 value=0 (低电平) 意味着继电器初始状态是“关闭”的。
    pump_relay = machine.Pin('B10', machine.Pin.OUT, value=0)
    print("✅ 水泵继电器引脚 (B10) 初始化成功 (高电平触发模式)")
except Exception as e:
    print(f"❌ 水泵继电器初始化失败: {e}")
    # 即使失败，程序也继续运行，只是水泵功能不可用

# --- 新增：初始化LED灯带继电器引脚 (B12) ---
try:
    # 同样假设为高电平触发，初始值 value=0 (关闭)
    led_strip_relay = machine.Pin('B12', machine.Pin.OUT, value=0)
    print("✅ LED灯带继电器引脚 (B12) 初始化成功 (高电平触发模式)")
except Exception as e:
    print(f"❌ LED灯带继电器初始化失败: {e}")

# --- 命令处理器 (修正为高电平触发逻辑) ---
def process_command(cmd):
    cmd = cmd.strip()
    
    # 优先尝试解析JSON格式的命令
    try:
        data = json.loads(cmd)
        actuator = data.get('actuator')
        action = data.get('action')

        if actuator == 'pump' and pump_relay:
            if action == 'on':
                pump_relay.high() # 高电平触发，打开继电器
                print('{"response": "Pump is ON"}')
            elif action == 'off':
                pump_relay.low() # 低电平，关闭继电器
                print('{"response": "Pump is OFF"}')
            else:
                print('{"error": "Unknown pump action"}')
        # --- 新增：处理LED灯带命令 ---
        elif actuator == 'led_strip' and led_strip_relay:
            if action == 'on':
                led_strip_relay.high() # 高电平，点亮灯带
                print('{"response": "LED Strip is ON"}')
            elif action == 'off':
                led_strip_relay.low() # 低电平，熄灭灯带
                print('{"response": "LED Strip is OFF"}')
            else:
                print('{"error": "Unknown led_strip action"}')
        else:
            print('{"error": "Unknown or unavailable actuator"}')
        return # JSON命令处理完毕，直接返回
        
    except (ValueError, KeyError):
        # 如果JSON解析失败，则回退到处理简单的字符串命令 (保持向后兼容)
        pass

    # --- 兼容旧的简单命令 ---
    if cmd == "led_on":
        status_led.low()
        print('{"response": "LED is ON"}')
    elif cmd == "led_off":
        status_led.high()
        print('{"response": "LED is OFF"}')
    else:
        # 对于无法解析的非JSON命令
        print(f'{{"error": "Unknown or invalid command: {cmd}"}}')

# --- 主循环 (核心代码未改变) ---
print("\n🚀 开始非阻塞数据采集与命令监听循环...")
print("-" * 50)
cycle_count = 0

# --- 任务调度相关的变量 ---
SENSOR_READ_INTERVAL = 1000  # 1秒读取一次传感器
last_sensor_read_time = time.ticks_ms()

poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

# --- 主循环 ---
while True:
    # 任务1: 检查并处理控制指令 (每次循环都做，所以响应极快)
    if poll_obj.poll(0):
        command = sys.stdin.readline()
        if command: # 确保读取到内容
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
        
    # 不再有大的 time.sleep()
    # time.sleep_ms(10) # 可以加一个非常小的延时，防止CPU 100% 占用

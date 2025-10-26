# 藏红花培育系统主程序 - v9.0 (集成PAJ7620手势识别)
# 在原有功能基础上，增加手势识别，并显示在OLED和Web界面

import machine
import time
import json
import sys
import select

# --- 导入驱动模块 ---
# 新增: 导入PAJ7620驱动
try:
    from drivers import create_dht11_sensor, get_driver_info
    import ssd1306 
    from paj7620 import PAJ7620
    
    # BH1750驱动类保持不变
    class BH1750:
        def __init__(self, i2c, addr=0x23):
            self.i2c = i2c; self.addr = addr; self.is_initialized = False
            try:
                self.i2c.writeto(self.addr, b'\x01'); time.sleep_ms(10)
                self.i2c.writeto(self.addr, b'\x10'); time.sleep_ms(120)
                self.is_initialized = True
            except Exception as e: print(f"❌ BH1750 初始化失败: {e}")
        def read_lux(self):
            if not self.is_initialized: return None
            try:
                data = self.i2c.readfrom(self.addr, 2)
                return ((data[0] << 8) | data[1]) / 1.2
            except: return None
            
    print("✅ 所有驱动模块加载成功")
except ImportError as e:
    print(f"❌ 关键驱动模块导入失败: {e}"); sys.exit()

print("\n=== 藏红花培育系统 v9.0 - 手势识别集成版 ===")

# --- 硬件与OLED配置 ---
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64
I2C_ADDRESS = 0x3C

# --- 硬件初始化 ---
status_led = machine.Pin('C13', machine.Pin.OUT, value=1)
dht11, light_sensor, soil_adc, paj_sensor = None, None, None, None
pump_relay, led_strip_relay = None, None
display = None # 初始化OLED显示对象

# DHT11 初始化
try: dht11 = create_dht11_sensor(machine.Pin('A1', machine.Pin.IN, machine.Pin.PULL_UP), 'DHT11')
except Exception as e: print(f"❌ DHT11 初始化失败: {e}")

# I2C总线、光照、OLED 和 手势传感器 初始化
try:
    # 固件会自动映射I2C(1)到 B6/B7, 无需指定引脚
    i2c = machine.I2C(1, freq=200000) # PAJ7620 推荐频率 <= 200kHz
    print("✅ I2C 总线初始化成功")

    # 初始化光照传感器
    light_sensor = BH1750(i2c)
    
    # 初始化OLED屏幕
    display = ssd1306.SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c, I2C_ADDRESS)
    print("✅ OLED 显示屏初始化成功")
    
    # --- 新增: 初始化手势传感器 ---
    paj_sensor = PAJ7620(i2c)
    paj_sensor.init()
    print("✅ PAJ7620 手势传感器初始化成功")
    
    # 显示启动画面
    display.fill(0)
    display.text('Saffron System', 8, 16)
    display.text('Gesture Ready!', 8, 32)
    display.show()
    time.sleep(2)

except Exception as e: 
    print(f"❌ I2C设备(光照/OLED/手势)初始化失败: {e}")

# 其他传感器和执行器初始化
try: soil_adc = machine.ADC(machine.Pin('A2'))
except Exception as e: print(f"❌ 土壤湿度传感器初始化失败: {e}")
try:
    pump_relay = machine.Pin('B10', machine.Pin.OUT, value=0)
    print("✅ 水泵继电器(B10)初始化成功")
except Exception as e: print(f"❌ 水泵继电器初始化失败: {e}")
try:
    led_strip_relay = machine.Pin('B12', machine.Pin.OUT, value=0)
    print("✅ LED灯带继电器(B12)初始化成功")
except Exception as e: print(f"❌ LED灯带继电器初始化失败: {e}")

# --- OLED 显示屏更新函数 ---
def update_display(data):
    """根据传入的数据包刷新OLED屏幕"""
    if not display: return # 如果屏幕未初始化，则不执行任何操作
    
    display.fill(0) # 清屏
    
    # 标题
    display.text("Saffron Monitor", 4, 0)
    display.hline(0, 10, 128, 1) # 分割线
    
    # 格式化显示数据 (如果值为None，则显示'--')
    temp_str = f"T:{data.get('temp', '--')}C"
    humi_str = f"H:{data.get('humi', '--')}%"
    lux_str  = f"L:{data.get('lux', '--')}"
    soil_str = f"S:{data.get('soil', '--')}%"
    
    # --- 新增: 手势信息显示 ---
    gesture_str = f"Ges: {data.get('gesture', 'None')}"
    
    # 在屏幕上分两列显示
    display.text(temp_str, 0, 16)
    display.text(humi_str, 64, 16)
    display.text(lux_str, 0, 32)
    display.text(soil_str, 64, 32)
    
    # 单独一行显示手势
    display.text(gesture_str, 0, 44)
    
    display.hline(0, 54, 128, 1) # 分割线
    display.text(f"C:{data.get('cycle', 0)}", 70, 56) # 循环计数

    display.show() # 将缓冲区内容推送到屏幕

# 命令处理器 (未修改)
def process_command(cmd):
    cmd = cmd.strip()
    try:
        data = json.loads(cmd)
        actuator, action = data.get('actuator'), data.get('action')
        response = None
        if actuator == 'pump' and pump_relay:
            if action == 'on': pump_relay.high(); response = '{"response": "Pump is ON"}'
            elif action == 'off': pump_relay.low(); response = '{"response": "Pump is OFF"}'
        elif actuator == 'led_strip' and led_strip_relay:
            if action == 'on': led_strip_relay.high(); response = '{"response": "LED Strip is ON"}'
            elif action == 'off': led_strip_relay.low(); response = '{"response": "LED Strip is OFF"}'
        
        if response: print(response)
        else: print('{"error": "Unknown or unavailable actuator"}')
    except (ValueError, KeyError):
        if cmd == "led_on": status_led.low(); print('{"response": "LED is ON"}')
        elif cmd == "led_off": status_led.high(); print('{"response": "LED is OFF"}')
        else: print(f'{{"error": "Unknown command: {cmd}"}}')

# --- 主循环 ---
print("\n🚀 开始主循环 (带手势识别)...")
print("-" * 50)
cycle_count = 0
SENSOR_READ_INTERVAL = 1000 # 1秒采集一次环境数据
last_sensor_read_time = time.ticks_ms()
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

# --- 新增: 手势状态变量 ---
last_valid_gesture = None
gesture_display_timer = 0
GESTURE_TIMEOUT = 3000  # 手势在数据包中保持有效的时间 (3秒)

while True:
    # 任务1: (高频) 检查手势
    if paj_sensor:
        try:
            gesture_name = paj_sensor.get_gesture_name(paj_sensor.get_gesture_code())
            if gesture_name:
                last_valid_gesture = gesture_name
                gesture_display_timer = time.ticks_ms()  # 发现新手势，重置计时器
        except Exception:
            pass # 忽略手势读取的偶尔错误

    # 任务2: 检查并处理控制指令
    if poll_obj.poll(0):
        command = sys.stdin.readline()
        if command: process_command(command)

    # 任务3: 定时读取传感器数据并发送
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_sensor_read_time) >= SENSOR_READ_INTERVAL:
        last_sensor_read_time = current_time
        cycle_count += 1
        
        # --- 新增: 检查手势是否超时 ---
        current_gesture = None
        if last_valid_gesture and time.ticks_diff(current_time, gesture_display_timer) < GESTURE_TIMEOUT:
            current_gesture = last_valid_gesture
        else:
            last_valid_gesture = None # 超时后清空

        # 采集数据
        data_packet = {"cycle": cycle_count, "timestamp": time.ticks_ms(), 
                       "temp": None, "humi": None, "lux": None, "soil": None,
                       "gesture": current_gesture} # 添加手势字段
                       
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
                DRY, WET = 59000, 26000
                if WET <= raw_value <= DRY + 2000:
                    p = 100 * (DRY - raw_value) / (DRY - WET)
                    data_packet['soil'] = round(max(0, min(100, p)))
            except: pass
                
        # 通过串口发送JSON数据到树莓派
        print(json.dumps(data_packet))
        
        # 在OLED上更新显示
        update_display(data_packet)
        
    time.sleep_ms(20) # 短暂延时，降低CPU占用率

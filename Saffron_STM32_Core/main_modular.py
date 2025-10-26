# 藏红花培育系统主程序 - v9.3 (执行器与UI布局修正版)
# - 修复手势控制执行器不响应的Bug (pin.toggle -> pin.value)
# - 优化主监控页UI，解决"Ges横条"问题

import machine
import time
import json
import sys
import select

# --- 导入驱动模块 ---
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

print("\n=== 藏红花培育系统 v9.3 - Bug修复版 ===")

# --- 硬件与OLED配置 ---
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64
I2C_ADDRESS = 0x3C

# --- OLED页面状态管理 ---
current_display_page = 0
NUM_PAGES = 3

# --- 硬件初始化 ---
status_led = machine.Pin('C13', machine.Pin.OUT, value=1)
dht11, light_sensor, soil_adc, paj_sensor = None, None, None, None
pump_relay, led_strip_relay = None, None
display = None

try: dht11 = create_dht11_sensor(machine.Pin('A1', machine.Pin.IN, machine.Pin.PULL_UP), 'DHT11')
except Exception as e: print(f"❌ DHT11 初始化失败: {e}")

try:
    i2c = machine.I2C(1, freq=200000)
    print("✅ I2C 总线初始化成功")
    light_sensor = BH1750(i2c)
    display = ssd1306.SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c, I2C_ADDRESS)
    print("✅ OLED 显示屏初始化成功")
    paj_sensor = PAJ7620(i2c)
    paj_sensor.init()
    print("✅ PAJ7620 手势传感器初始化成功")
    display.fill(0)
    display.text('Saffron System', 8, 16)
    display.text('Gesture Ready!', 8, 32)
    display.show()
    time.sleep(2)
except Exception as e:
    print(f"❌ I2C设备(光照/OLED/手势)初始化失败: {e}")

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

# --- OLED 显示屏更新函数 (UI布局优化) ---
def update_display(data, page_num):
    if not display: return
    display.fill(0)
    page_indicator = f"[{page_num + 1}/{NUM_PAGES}]"

    # --- 页面 1: 主监控页 (优化布局) ---
    if page_num == 0:
        display.text("Saffron Monitor", 4, 0)
        display.text("----------------", 0, 9)
        temp_str = f"T:{data.get('temp', '--')}C"
        humi_str = f"H:{data.get('humi', '--')}%"
        lux_str  = f"L:{data.get('lux', '--')}"
        soil_str = f"S:{data.get('soil', '--')}%"
        display.text(temp_str, 0, 19)
        display.text(humi_str, 64, 19)
        display.text(lux_str, 0, 35)
        display.text(soil_str, 64, 35)
        
        # 将手势信息移到最底行左侧
        gesture_text = f"G:{data.get('gesture', '--')}"
        display.text(gesture_text, 0, 55)

    # --- 页面 2: 设备控制页 ---
    elif page_num == 1:
        display.text("Device Control", 4, 0)
        display.text("----------------", 0, 9)
        pump_state = "ON" if pump_relay and pump_relay.value() else "OFF"
        led_state = "ON" if led_strip_relay and led_strip_relay.value() else "OFF"
        display.text(f"Water Pump : {pump_state}", 0, 20)
        display.text(f"LED Strip  : {led_state}", 0, 34)
        display.text("Up/Down:Pump|Wave:LED", 0, 51)

    # --- 页面 3: 系统信息页 ---
    elif page_num == 2:
        display.text("System Info", 4, 0)
        display.text("----------------", 0, 9)
        driver_mode = dht11.driver_mode if dht11 else "N/A"
        display.text(f"DHT Driver:{driver_mode}", 0, 20)
        display.text(f"Cycle Count:{data.get('cycle', 0)}", 0, 34)
        py_ver = f"{sys.version_info[0]}.{sys.version_info[1]}"
        display.text(f"MicroPython: v{py_ver}", 0, 48)

    # 在右下角显示页码指示器
    display.text(page_indicator, 128 - len(page_indicator) * 8 - 2, 55)
    display.show()

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
print("\n🚀 开始主循环 (Bug修复版)...")
print("-" * 50)
cycle_count = 0
SENSOR_READ_INTERVAL = 1000 # 1秒
last_sensor_read_time = time.ticks_ms()
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

last_valid_gesture = None
gesture_display_timer = 0
GESTURE_TIMEOUT = 3000
last_gesture_process_time = 0
GESTURE_COOLDOWN = 500
current_data_packet = {"cycle": 0, "gesture": None}

while True:
    current_time = time.ticks_ms()

    # 任务1: (高频) 检查并处理手势
    if paj_sensor and time.ticks_diff(current_time, last_gesture_process_time) > GESTURE_COOLDOWN:
        try:
            gesture_name = paj_sensor.get_gesture_name(paj_sensor.get_gesture_code())
            if gesture_name:
                last_valid_gesture = gesture_name
                gesture_display_timer = current_time
                last_gesture_process_time = current_time
                needs_display_update = False

                if gesture_name == "向右":
                    current_display_page = (current_display_page + 1) % NUM_PAGES
                    needs_display_update = True
                elif gesture_name == "向左":
                    current_display_page = (current_display_page - 1 + NUM_PAGES) % NUM_PAGES
                    needs_display_update = True
                
                # 在“设备控制页”时，响应控制手势
                elif current_display_page == 1:
                    # --- CRITICAL FIX: 使用正确的 pin.value() 进行状态翻转 ---
                    if gesture_name in ("向上", "向下") and pump_relay:
                        pump_relay.value(not pump_relay.value())
                        needs_display_update = True
                        print(f'{{"event":"gesture_control", "actuator":"pump", "new_state":{pump_relay.value()}}}')
                    elif gesture_name == "挥手" and led_strip_relay:
                        led_strip_relay.value(not led_strip_relay.value())
                        needs_display_update = True
                        print(f'{{"event":"gesture_control", "actuator":"led_strip", "new_state":{led_strip_relay.value()}}}')

                if needs_display_update:
                    update_display(current_data_packet, current_display_page)
        except Exception:
            pass

    # 任务2: 检查并处理来自树莓派的控制指令
    if poll_obj.poll(0):
        command = sys.stdin.readline()
        if command: 
            process_command(command)
            if current_display_page == 1:
                 update_display(current_data_packet, current_display_page)

    # 任务3: 定时读取传感器数据并发送/刷新
    if time.ticks_diff(current_time, last_sensor_read_time) >= SENSOR_READ_INTERVAL:
        last_sensor_read_time = current_time
        cycle_count += 1
        
        current_gesture_for_pi = None
        if last_valid_gesture and time.ticks_diff(current_time, gesture_display_timer) < GESTURE_TIMEOUT:
            current_gesture_for_pi = last_valid_gesture
        else:
            last_valid_gesture = None
            
        current_data_packet = {
            "cycle": cycle_count, "timestamp": time.ticks_ms(), 
            "temp": None, "humi": None, "lux": None, "soil": None,
            "gesture": current_gesture_for_pi
        } 
                       
        if dht11 and dht11.measure():
            sensor_data = dht11.get_data()
            if sensor_data.get('is_valid'):
                current_data_packet['temp'] = sensor_data.get('temperature')
                current_data_packet['humi'] = sensor_data.get('humidity')
        if light_sensor:
            lux_val = light_sensor.read_lux()
            if lux_val is not None: current_data_packet['lux'] = round(lux_val, 1)
        if soil_adc:
            try:
                raw_value = soil_adc.read_u16()
                DRY, WET = 59000, 26000
                if WET <= raw_value <= DRY + 2000:
                    p = 100 * (DRY - raw_value) / (DRY - WET)
                    current_data_packet['soil'] = round(max(0, min(100, p)))
            except: pass
                
        print(json.dumps(current_data_packet))
        update_display(current_data_packet, current_display_page)
        
    time.sleep_ms(20)

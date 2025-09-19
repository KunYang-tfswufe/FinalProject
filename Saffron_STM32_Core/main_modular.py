# 藏红花培育系统主程序 - 模块化版本 v7.0
# 集成温湿度、光照、土壤湿度传感器

import machine
import time
import json
import sys

# 导入所有需要的驱动
try:
    from drivers import create_dht11_sensor, get_driver_info
    # 我们需要一个光照传感器的驱动，这里我们假设它叫 'bh1750.py'
    # 为了简化，我们直接在这里定义一个简单的光照传感器类
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
                # print(f"光照读取错误: {e}") # 调试时可以取消注释
                return None
                
    print("✅ 所有驱动模块加载成功")

except ImportError as e:
    print(f"❌ 关键驱动模块导入失败: {e}, 系统无法启动。")
    sys.exit()

print("\n=== 藏红花培育系统 v7.0 - 多传感器集成 ===")

# --- 硬件初始化 ---

# 1. 状态LED
try:
    status_led = machine.Pin('C13', machine.Pin.OUT)
    status_led.high()  # 初始熄灭
    print("✅ 系统LED初始化成功")
except Exception as e:
    status_led = None

# 2. DHT11 温湿度传感器
try:
    print("\n[1/3] 初始化 DHT11 温湿度传感器...")
    sensor_pin = machine.Pin('A1', machine.Pin.IN, machine.Pin.PULL_UP)
    dht11 = create_dht11_sensor(sensor_pin, 'DHT11')
    print(f"✅ DHT11 初始化成功 (驱动模式: {dht11.driver_mode})")
except Exception as e:
    print(f"❌ DHT11 初始化失败: {e}")
    dht11 = None

# 3. BH1750 光照传感器
try:
    print("\n[2/3] 初始化 BH1750 光照传感器...")
    i2c = machine.I2C(1, freq=100000)
    # 扫描I2C总线，帮助调试
    devices = i2c.scan()
    if not devices:
        print("   - 警告: I2C总线上未发现任何设备！")
    else:
        print(f"   - I2C扫描发现设备: {[hex(d) for d in devices]}")
        
    light_sensor = BH1750(i2c)
except Exception as e:
    print(f"❌ I2C或光照传感器初始化失败: {e}")
    light_sensor = None

# 4. 土壤湿度传感器 (ADC)
try:
    print("\n[3/3] 初始化土壤湿度传感器...")
    soil_adc = machine.ADC(machine.Pin('A2'))
    print("✅ 土壤湿度传感器初始化成功")
except Exception as e:
    print(f"❌ 土壤湿度传感器初始化失败: {e}")
    soil_adc = None


# --- 主循环 ---
print("\n🚀 开始多传感器数据采集循环...")
print("-" * 50)
cycle_count = 0

while True:
    cycle_count += 1
    
    # 最终发送到树莓派的数据包
    data_packet = {
        "temp": None,
        "humi": None,
        "lux": None,
        "soil": None,
        "cycle": cycle_count,
        "timestamp": time.ticks_ms()
    }
    
    # --- 逐个采集传感器数据 ---

    # 1. 读取温湿度
    if dht11 and dht11.measure():
        sensor_data = dht11.get_data()
        if sensor_data.get('is_valid'):
            data_packet['temp'] = sensor_data.get('temperature')
            data_packet['humi'] = sensor_data.get('humidity')

    # 2. 读取光照强度
    if light_sensor:
        lux_val = light_sensor.read_lux()
        if lux_val is not None:
             data_packet['lux'] = round(lux_val, 1) # 保留一位小数

    # 3. 读取土壤湿度
    if soil_adc:
        try:
            raw_value = soil_adc.read_u16()
            # 简单的范围检查，避免悬空时的噪声读数 (0-65535)
            # 这个范围需要根据你的传感器在干燥空气中和浸入水中的读数来校准
            # 常见电容式传感器：空气中约 58000-60000，水中约 25000-27000
            # 假设干（空气）读数 59000，湿（水）读数 26000
            DRY_VALUE = 59000
            WET_VALUE = 26000
            
            if WET_VALUE <= raw_value <= DRY_VALUE + 2000: # 加一点容错
                # 将读数映射到 0-100%
                percentage = 100 * (DRY_VALUE - raw_value) / (DRY_VALUE - WET_VALUE)
                data_packet['soil'] = round(max(0, min(100, percentage))) # 限制在0-100之间
        except Exception:
            pass # 读取失败则为None

    # --- 数据处理与发送 ---
    
    # 将完整数据包转换为JSON字符串
    json_string = json.dumps(data_packet)
    
    # 通过串口打印输出
    print(json_string)
    
    # 成功指示：LED短闪一下
    if status_led:
        status_led.low()
        time.sleep_ms(50)
        status_led.high()
        
    # 每3秒重复一次循环
    time.sleep(3)

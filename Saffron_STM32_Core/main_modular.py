# 藏红花培育系统主程序 - 模块化版本
# 版本 6.0 - 使用专业的模块化驱动架构

import machine
import time
import json
import sys

print("=== 藏红花培育系统 v6.0 - 模块化版本 ===")
print("使用专业模块化传感器驱动")

# 初始化状态LED
try:
    status_led = machine.Pin('C13', machine.Pin.OUT)
    status_led.high()  # 熄灭LED
    print("✅ 系统LED初始化成功")
except Exception as e:
    print(f"⚠️ LED初始化失败: {e}")
    status_led = None

# 导入模块化传感器驱动
try:
    from drivers import create_dht11_sensor, get_driver_info, SensorError
    print("✅ 模块化传感器驱动导入成功")
    
    # 显示驱动模块信息
    driver_info = get_driver_info()
    print(f"📦 驱动版本: {driver_info['version']}")
    print(f"🔧 硬件DHT支持: {'是' if driver_info['hardware_dht_support'] else '否'}")
    print(f"📊 平台: {driver_info['platform']}")
    
except ImportError as e:
    print(f"❌ 驱动模块导入失败: {e}")
    print("系统无法启动")
    exit()

# 初始化DHT11传感器
try:
    print("\n🌡️ 初始化DHT11温湿度传感器...")
    sensor_pin = machine.Pin('A1', machine.Pin.IN, machine.Pin.PULL_UP)
    dht11 = create_dht11_sensor(sensor_pin, 'DHT11')
    
    if not dht11.is_ready():
        raise Exception("传感器未就绪")
    
    print(f"✅ 传感器初始化成功 (使用{dht11.driver_mode}驱动)")
    
    # 启动指示：根据驱动类型闪烁不同模式
    if status_led:
        if dht11.driver_mode == "hardware":
            # 硬件模式：快速闪烁5次
            for _ in range(5):
                status_led.low()
                time.sleep_ms(100)
                status_led.high()
                time.sleep_ms(100)
        elif dht11.driver_mode == "software":
            # 软件模式：中速闪烁3次  
            for _ in range(3):
                status_led.low()
                time.sleep_ms(200)
                status_led.high()
                time.sleep_ms(200)
        else:
            # 模拟模式：慢速闪烁2次
            for _ in range(2):
                status_led.low()
                time.sleep_ms(400)
                status_led.high()
                time.sleep_ms(400)
    
except Exception as e:
    print(f"❌ 传感器初始化失败: {e}")
    print("系统无法启动")
    exit()

# 显示初始传感器状态
print("\n📊 传感器状态报告:")
print("-" * 40)
status = dht11.get_status()
for key, value in status.items():
    print(f"   {key}: {value}")

print("\n🚀 开始数据采集循环...")
print(f"💡 当前驱动模式: {dht11.driver_mode}")
print("-" * 50)

# 主数据采集循环
cycle_count = 0

while True:
    cycle_count += 1
    try:
        # 1. 执行测量
        measurement_ok = dht11.measure()
        
        if measurement_ok:
            # 2. 获取数据
            sensor_data = dht11.get_data()
            
            if sensor_data.get('is_valid'):
                # 3. 构建数据包
                data_packet = {
                    "temp": sensor_data.get('temperature'),
                    "humi": sensor_data.get('humidity'),
                    "cycle": cycle_count,
                    "driver": sensor_data.get('driver_mode'),
                    "success_rate": dht11.get_status().get('success_rate'),
                    "timestamp": time.ticks_ms()
                }
                
                # 4. 打印 JSON (这是与树莓派通信的关键)
                print(json.dumps(data_packet))
                
                # 5. 成功闪灯
                if status_led:
                    status_led.low()
                    time.sleep_ms(50)
                    status_led.high()
            else:
                print("# 错误: 传感器返回无效数据")

        else:
            print("# 错误: 传感器测量失败")

    except Exception as e:
        # 捕获任何意外错误
        print(f"# 系统错误 #{cycle_count}: {e}")
    
    # 6. 等待下一个周期 (固定2秒，方便调试)
    time.sleep(2)

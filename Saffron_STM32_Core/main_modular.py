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
    try:
        cycle_count += 1
        
        # 执行传感器测量
        if dht11.measure():
            # 获取传感器数据
            sensor_data = dht11.get_data()
            
            if sensor_data['is_valid']:
                # 构建完整的数据包
                data_packet = {
                    "temp": sensor_data['temperature'],
                    "humi": sensor_data['humidity'],
                    "cycle": cycle_count,
                    "driver": sensor_data['driver_mode'],
                    "sensor_type": sensor_data['sensor_type'],
                    "timestamp": time.ticks_ms(),
                    "system_version": "6.0_modular"
                }
                
                # 添加传感器状态信息
                current_status = dht11.get_status()
                data_packet["success_rate"] = current_status['success_rate']
                data_packet["total_reads"] = current_status['read_count']
                
                # 输出JSON数据到串口（供Flask服务器接收）
                json_string = json.dumps(data_packet)
                print(json_string)
                sys.stdout.flush()  # 确保数据立即输出
                
                # 成功指示：LED短闪
                if status_led:
                    status_led.low()
                    time.sleep_ms(50)
                    status_led.high()
                    
            else:
                raise SensorError("传感器返回无效数据")
                
        else:
            raise SensorError("传感器测量失败")
            
    except SensorError as e:
        print(f"❌ 传感器错误 #{cycle_count}: {e}")
        
        # 传感器错误指示：双闪
        if status_led:
            for _ in range(2):
                status_led.low()
                time.sleep_ms(150)
                status_led.high()
                time.sleep_ms(150)
                
    except Exception as e:
        print(f"❌ 系统错误 #{cycle_count}: {e}")
        
        # 系统错误指示：三闪
        if status_led:
            for _ in range(3):
                status_led.low()
                time.sleep_ms(100)
                status_led.high()
                time.sleep_ms(100)
    
    # 周期性状态报告（每20个周期）
    if cycle_count % 20 == 0:
        status = dht11.get_status()
        print(f"# 📊 系统运行报告 (周期 {cycle_count}):")
        print(f"#    成功率: {status['success_rate']}")
        print(f"#    驱动模式: {dht11.driver_mode}")
        print(f"#    总读取次数: {status['read_count']}")
        print(f"#    错误次数: {status['error_count']}")
        
        # 检查是否需要重置统计
        if status['error_count'] > 100:
            print("# 🔄 重置传感器统计信息...")
            dht11.reset_statistics()
    
    # 智能延迟调整
    current_status = dht11.get_status()
    error_rate = float(current_status['success_rate'].rstrip('%'))
    
    if error_rate >= 90:
        sleep_time = 2      # 高成功率：2秒间隔
    elif error_rate >= 70:
        sleep_time = 3      # 中成功率：3秒间隔  
    elif error_rate >= 50:
        sleep_time = 5      # 低成功率：5秒间隔
    else:
        sleep_time = 8      # 很低成功率：8秒间隔
    
    # 模拟数据模式使用固定间隔
    if dht11.driver_mode == "simulated":
        sleep_time = 2
    
    time.sleep(sleep_time)

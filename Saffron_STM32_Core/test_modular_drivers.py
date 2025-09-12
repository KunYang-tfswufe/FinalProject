# 模块化驱动测试程序
# 测试drivers模块的功能

import machine
import time
import json

print("=== 模块化传感器驱动测试 ===")
print("测试新的drivers模块结构")

# 初始化LED
try:
    led = machine.Pin('C13', machine.Pin.OUT)
    led.high()  # 熄灭
    print("✅ LED初始化成功")
except:
    led = None

try:
    # 导入模块化的驱动
    from drivers import create_dht11_sensor, get_driver_info
    
    print("✅ 成功导入模块化驱动")
    
    # 显示驱动信息
    print("\n📊 驱动模块信息:")
    print("-" * 30)
    info = get_driver_info()
    for key, value in info.items():
        print(f"   {key}: {value}")
    
    # 创建传感器实例
    print("\n🔧 创建DHT11传感器实例...")
    sensor_pin = machine.Pin('A1', machine.Pin.IN, machine.Pin.PULL_UP)
    dht11 = create_dht11_sensor(sensor_pin, 'DHT11')
    
    print("✅ DHT11传感器实例创建成功")
    
    # 显示传感器状态
    print("\n📊 传感器状态:")
    print("-" * 30)
    status = dht11.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    # 进行多次测试
    print(f"\n🔬 开始传感器测试 (使用{dht11.driver_mode}驱动)")
    print("=" * 50)
    
    success_count = 0
    total_tests = 8
    
    for i in range(total_tests):
        print(f"\n📊 测试 #{i+1}/{total_tests}")
        print("-" * 25)
        
        try:
            # 执行测量
            if dht11.measure():
                # 获取数据
                data = dht11.get_data()
                
                if data['is_valid']:
                    success_count += 1
                    
                    print(f"✅ 测量成功!")
                    print(f"   温度: {data['temperature']}°C")
                    print(f"   湿度: {data['humidity']}%")
                    print(f"   驱动: {data['driver_mode']}")
                    
                    # JSON输出
                    json_output = {
                        "temp": data['temperature'],
                        "humi": data['humidity'],
                        "test": i + 1,
                        "driver": data['driver_mode'],
                        "sensor": data['sensor_type']
                    }
                    print(f"📤 JSON: {json.dumps(json_output)}")
                    
                    # 成功指示
                    if led:
                        led.low()
                        time.sleep_ms(100)
                        led.high()
                else:
                    print("❌ 数据无效")
            else:
                print("❌ 测量失败")
                
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            
            # 错误指示
            if led:
                for _ in range(2):
                    led.toggle()
                    time.sleep_ms(150)
        
        # 显示当前传感器状态
        current_status = dht11.get_status()
        print(f"   成功率: {current_status['success_rate']}")
        print(f"   驱动模式: {dht11.driver_mode}")
        
        time.sleep(2)  # 测试间隔
    
    # 最终统计
    print("\n" + "=" * 50)
    print("🏁 模块化驱动测试总结")
    print("=" * 50)
    
    final_status = dht11.get_status()
    print(f"📈 测试统计:")
    print(f"   总测试次数: {final_status['read_count']}")
    print(f"   成功次数: {final_status['read_count'] - final_status['error_count']}")
    print(f"   成功率: {final_status['success_rate']}")
    print(f"   使用驱动: {dht11.driver_mode}")
    print(f"   传感器类型: {dht11.sensor_type}")
    
    # 评估结果
    success_rate = float(final_status['success_rate'].rstrip('%'))
    if success_rate >= 80:
        print("🎉 模块化驱动工作优秀!")
        result_icon = "🏆"
    elif success_rate >= 60:
        print("✅ 模块化驱动工作良好!")
        result_icon = "👍"
    elif success_rate >= 30:
        print("⚠️ 模块化驱动基本可用")
        result_icon = "⚠️"
    else:
        print("❌ 模块化驱动需要调试")
        result_icon = "🔧"
    
    # 最终指示
    if led:
        # 根据结果闪烁不同次数
        if success_rate >= 80:
            flash_count = 5  # 优秀：5次
        elif success_rate >= 60:
            flash_count = 3  # 良好：3次
        else:
            flash_count = 1  # 需要改进：1次
        
        for _ in range(flash_count):
            led.low()
            time.sleep_ms(200)
            led.high()
            time.sleep_ms(200)
    
    print(f"\n{result_icon} 模块化驱动测试完成")
    
    # 模块API展示
    print(f"\n📚 模块API使用示例:")
    print("```python")
    print("from drivers import create_dht11_sensor")
    print("import machine")
    print("")
    print("pin = machine.Pin('A1', machine.Pin.IN, machine.Pin.PULL_UP)")
    print("sensor = create_dht11_sensor(pin, 'DHT11')")
    print("")
    print("if sensor.measure():")
    print("    data = sensor.get_data()")
    print("    print(f\"温度: {data['temperature']}°C\")")
    print("    print(f\"湿度: {data['humidity']}%\")")
    print("```")
    
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    print("\n可能的原因:")
    print("1. drivers文件夹中的文件未正确上传")
    print("2. __init__.py文件有语法错误")
    print("3. 模块依赖关系有问题")
    
except Exception as e:
    print(f"❌ 测试异常: {e}")
    print("请检查模块结构和代码")

print("\n🔚 测试程序结束")

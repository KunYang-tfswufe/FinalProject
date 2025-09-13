# 藏红花培育系统 - 全面功能测试
import machine
import time
import json
import sys

print("=" * 60)
print("🌱 藏红花培育系统 - 全面功能测试")
print("=" * 60)

# 测试结果统计
test_results = {
    'hardware_init': False,
    'dht11_sensor': False,
    'light_sensor': False,
    'soil_sensor': False,
    'led_control': False,
    'serial_communication': False,
    'json_output': False,
    'error_handling': False
}

def test_hardware_initialization():
    """测试硬件初始化"""
    print("\n1️⃣ 测试硬件初始化...")
    try:
        # 测试LED
        led = machine.Pin('C13', machine.Pin.OUT)
        led.high()
        print("   ✅ LED初始化成功")
        
        # 测试I2C
        i2c = machine.I2C(1, freq=100000)
        devices = i2c.scan()
        print(f"   ✅ I2C初始化成功，检测到设备: {[hex(d) for d in devices]}")
        
        # 测试ADC
        adc = machine.ADC(machine.Pin('A2'))
        print("   ✅ ADC初始化成功")
        
        test_results['hardware_init'] = True
        return True
    except Exception as e:
        print(f"   ❌ 硬件初始化失败: {e}")
        return False

def test_dht11_sensor():
    """测试DHT11温湿度传感器"""
    print("\n2️⃣ 测试DHT11温湿度传感器...")
    try:
        from dht import DHT11
        sensor_pin = machine.Pin('A1', machine.Pin.IN, machine.Pin.PULL_UP)
        dht11 = DHT11(sensor_pin)
        
        # 测试多次读取
        success_count = 0
        for i in range(5):
            try:
                dht11.measure()
                temp = dht11.temperature()
                humi = dht11.humidity()
                print(f"   第{i+1}次: 温度={temp}°C, 湿度={humi}%")
                if temp is not None and humi is not None:
                    success_count += 1
            except Exception as e:
                print(f"   第{i+1}次: 读取失败 - {e}")
            time.sleep_ms(1000)
        
        if success_count >= 3:
            print(f"   ✅ DHT11传感器测试通过 ({success_count}/5 成功)")
            test_results['dht11_sensor'] = True
            return True
        else:
            print(f"   ❌ DHT11传感器测试失败 ({success_count}/5 成功)")
            return False
            
    except Exception as e:
        print(f"   ❌ DHT11传感器初始化失败: {e}")
        return False

def test_light_sensor():
    """测试光照传感器"""
    print("\n3️⃣ 测试光照传感器...")
    try:
        i2c = machine.I2C(1, freq=100000)
        addr = 0x23
        
        # 初始化BH1750
        i2c.writeto(addr, b'\x07')  # Reset
        time.sleep_ms(10)
        i2c.writeto(addr, b'\x01')  # Power On
        time.sleep_ms(10)
        i2c.writeto(addr, b'\x10')  # 连续高分辨率模式
        time.sleep_ms(180)
        
        # 测试多次读取
        values = []
        for i in range(5):
            try:
                data = i2c.readfrom(addr, 2)
                raw_value = (data[0] << 8) | data[1]
                lux = raw_value / 1.2
                values.append(raw_value)
                print(f"   第{i+1}次: 原始={raw_value}, 光照={lux:.2f} lux")
                time.sleep_ms(1000)
            except Exception as e:
                print(f"   第{i+1}次: 读取失败 - {e}")
        
        # 检查是否有变化
        if len(values) > 1 and max(values) != min(values):
            print("   ✅ 光照传感器有变化，测试通过")
            test_results['light_sensor'] = True
            return True
        else:
            print("   ⚠️ 光照传感器数值无变化，可能有问题")
            test_results['light_sensor'] = False
            return False
            
    except Exception as e:
        print(f"   ❌ 光照传感器测试失败: {e}")
        return False

def test_soil_sensor():
    """测试土壤湿度传感器"""
    print("\n4️⃣ 测试土壤湿度传感器...")
    try:
        soil_adc = machine.ADC(machine.Pin('A2'))
        
        # 测试多次读取
        values = []
        for i in range(5):
            try:
                raw_value = soil_adc.read_u16()
                if 1000 < raw_value < 50000:  # 合理范围
                    soil_percent = max(0, min(100, (65535 - raw_value) * 100 // 65535))
                    values.append(soil_percent)
                    print(f"   第{i+1}次: 原始={raw_value}, 湿度={soil_percent}%")
                else:
                    print(f"   第{i+1}次: 原始={raw_value}, 数据异常")
                time.sleep_ms(500)
            except Exception as e:
                print(f"   第{i+1}次: 读取失败 - {e}")
        
        if len(values) > 0:
            print(f"   ✅ 土壤湿度传感器测试通过，平均湿度: {sum(values)/len(values):.1f}%")
            test_results['soil_sensor'] = True
            return True
        else:
            print("   ❌ 土壤湿度传感器测试失败")
            return False
            
    except Exception as e:
        print(f"   ❌ 土壤湿度传感器测试失败: {e}")
        return False

def test_led_control():
    """测试LED控制"""
    print("\n5️⃣ 测试LED控制...")
    try:
        led = machine.Pin('C13', machine.Pin.OUT)
        
        # 测试LED闪烁
        print("   测试LED闪烁模式...")
        for i in range(3):
            led.low()   # 亮
            time.sleep_ms(200)
            led.high()  # 灭
            time.sleep_ms(200)
        
        print("   ✅ LED控制测试通过")
        test_results['led_control'] = True
        return True
        
    except Exception as e:
        print(f"   ❌ LED控制测试失败: {e}")
        return False

def test_serial_communication():
    """测试串口通信"""
    print("\n6️⃣ 测试串口通信...")
    try:
        # 测试JSON数据输出
        test_data = {
            "test": True,
            "timestamp": time.ticks_ms(),
            "message": "串口通信测试"
        }
        
        json_string = json.dumps(test_data)
        print(f"   发送测试数据: {json_string}")
        print(json_string)
        sys.stdout.flush()
        
        print("   ✅ 串口通信测试通过")
        test_results['serial_communication'] = True
        return True
        
    except Exception as e:
        print(f"   ❌ 串口通信测试失败: {e}")
        return False

def test_json_output():
    """测试JSON数据输出"""
    print("\n7️⃣ 测试JSON数据输出...")
    try:
        # 模拟完整的数据包
        data_packet = {
            "temp": 25,
            "humi": 60,
            "lux": 100.5,
            "soil": 45,
            "cycle": 1,
            "timestamp": time.ticks_ms(),
            "system_version": "test_v1.0"
        }
        
        json_string = json.dumps(data_packet)
        print(f"   完整数据包: {json_string}")
        print(json_string)
        sys.stdout.flush()
        
        print("   ✅ JSON数据输出测试通过")
        test_results['json_output'] = True
        return True
        
    except Exception as e:
        print(f"   ❌ JSON数据输出测试失败: {e}")
        return False

def test_error_handling():
    """测试错误处理"""
    print("\n8️⃣ 测试错误处理...")
    try:
        # 测试异常捕获
        try:
            # 故意制造一个错误
            invalid_pin = machine.Pin('Z99', machine.Pin.OUT)
        except Exception as e:
            print(f"   异常捕获测试: {e}")
        
        # 测试JSON解析错误处理
        try:
            invalid_json = json.loads("invalid json")
        except Exception as e:
            print(f"   JSON错误处理: {e}")
        
        print("   ✅ 错误处理测试通过")
        test_results['error_handling'] = True
        return True
        
    except Exception as e:
        print(f"   ❌ 错误处理测试失败: {e}")
        return False

def run_comprehensive_test():
    """运行全面测试"""
    print("开始全面功能测试...")
    
    # 运行所有测试
    tests = [
        test_hardware_initialization,
        test_dht11_sensor,
        test_light_sensor,
        test_soil_sensor,
        test_led_control,
        test_serial_communication,
        test_json_output,
        test_error_handling
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed_tests += 1
        except Exception as e:
            print(f"   ❌ 测试异常: {e}")
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    for test_name, result in test_results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name:20}: {status}")
    
    print(f"\n总体结果: {passed_tests}/{total_tests} 测试通过")
    
    if passed_tests == total_tests:
        print("🎉 所有测试通过！系统运行正常！")
    elif passed_tests >= total_tests * 0.8:
        print("⚠️ 大部分测试通过，系统基本正常")
    else:
        print("❌ 多个测试失败，需要检查系统")
    
    return passed_tests, total_tests

# 运行测试
if __name__ == "__main__":
    run_comprehensive_test()

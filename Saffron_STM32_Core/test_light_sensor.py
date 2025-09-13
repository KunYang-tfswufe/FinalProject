# BH1750 光照传感器完整测试程序
import machine
import time
import json

print("=== BH1750 光照传感器完整测试 ===")

# 初始化I2C
i2c = machine.I2C(1, freq=100000)
addr = 0x23

def reset_sensor():
    """重置传感器"""
    try:
        i2c.writeto(addr, b'\x07')  # Reset
        time.sleep_ms(10)
        print("✅ 传感器重置完成")
    except Exception as e:
        print(f"❌ 重置失败: {e}")

def power_on_sensor():
    """开启传感器电源"""
    try:
        i2c.writeto(addr, b'\x01')  # Power On
        time.sleep_ms(10)
        print("✅ 传感器电源开启")
    except Exception as e:
        print(f"❌ 电源开启失败: {e}")

def read_light(mode=0x10, mode_name="连续高分辨率"):
    """读取光照值"""
    try:
        # 发送测量命令
        i2c.writeto(addr, bytes([mode]))
        
        # 等待测量完成 (不同模式需要不同时间)
        if mode in [0x10, 0x13]:  # 连续模式
            time.sleep_ms(120)
        else:  # 一次性模式
            time.sleep_ms(180)
        
        # 读取数据
        data = i2c.readfrom(addr, 2)
        raw_value = (data[0] << 8) | data[1]
        lux = raw_value / 1.2
        
        return {
            'raw': raw_value,
            'lux': lux,
            'mode': mode_name,
            'data_bytes': data
        }
    except Exception as e:
        return {'error': str(e)}

# 主测试程序
print("\n1. 初始化传感器...")
reset_sensor()
power_on_sensor()

print("\n2. 测试不同测量模式...")
modes = [
    (0x10, "连续高分辨率"),
    (0x13, "连续低分辨率"), 
    (0x20, "一次性高分辨率"),
    (0x23, "一次性低分辨率")
]

for mode_code, mode_name in modes:
    print(f"\n--- 测试 {mode_name} 模式 ---")
    
    # 连续测量5次
    for i in range(5):
        result = read_light(mode_code, mode_name)
        if 'error' in result:
            print(f"  第{i+1}次: 错误 - {result['error']}")
        else:
            print(f"  第{i+1}次: 原始={result['raw']}, 光照={result['lux']:.2f} lux")
        
        time.sleep_ms(1000)  # 等待1秒

print("\n3. 长时间测试 (请用手遮挡传感器)...")
print("   现在开始30秒连续测量，请用手遮挡传感器观察数值变化...")

# 使用连续高分辨率模式进行长时间测试
i2c.writeto(addr, b'\x01')  # Power On
time.sleep_ms(10)
i2c.writeto(addr, b'\x10')  # 连续高分辨率模式
time.sleep_ms(120)

for i in range(30):
    try:
        data = i2c.readfrom(addr, 2)
        raw_value = (data[0] << 8) | data[1]
        lux = raw_value / 1.2
        
        print(f"  第{i+1:2d}秒: 原始={raw_value:3d}, 光照={lux:6.2f} lux")
        time.sleep_ms(1000)
    except Exception as e:
        print(f"  第{i+1:2d}秒: 错误 - {e}")

print("\n=== 测试完成 ===")

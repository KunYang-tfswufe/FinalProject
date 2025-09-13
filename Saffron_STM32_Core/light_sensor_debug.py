# 光照传感器调试程序
import machine
import time

print("=== 光照传感器调试程序 ===")

# 初始化I2C
i2c = machine.I2C(1, freq=100000)
addr = 0x23

print("1. 检查I2C设备...")
devices = i2c.scan()
print(f"   检测到的设备: {[hex(d) for d in devices]}")

if addr not in devices:
    print(f"   ❌ 地址 {hex(addr)} 未找到")
    exit()

print("2. 初始化BH1750...")
try:
    # 重置传感器
    i2c.writeto(addr, b'\x07')  # Reset
    time.sleep_ms(10)
    print("   ✅ 重置完成")
    
    # 电源开启
    i2c.writeto(addr, b'\x01')  # Power On
    time.sleep_ms(10)
    print("   ✅ 电源开启")
    
    # 设置连续高分辨率模式
    i2c.writeto(addr, b'\x10')  # 连续高分辨率模式
    time.sleep_ms(180)
    print("   ✅ 设置连续高分辨率模式")
    
except Exception as e:
    print(f"   ❌ 初始化失败: {e}")
    exit()

print("3. 开始连续测试 (请用手遮挡传感器)...")
print("   现在开始30秒测试，请用手遮挡传感器观察数值变化...")

for i in range(30):
    try:
        # 读取数据
        data = i2c.readfrom(addr, 2)
        raw_value = (data[0] << 8) | data[1]
        lux = raw_value / 1.2
        
        # 检查数据是否变化
        if i == 0:
            last_raw = raw_value
            change_count = 0
        else:
            if raw_value != last_raw:
                change_count += 1
                last_raw = raw_value
        
        status = "📊 变化" if raw_value != last_raw else "🔒 固定"
        print(f"   第{i+1:2d}秒: 原始={raw_value:3d}, 光照={lux:6.2f} lux {status}")
        
        time.sleep_ms(1000)
    except Exception as e:
        print(f"   第{i+1:2d}秒: 错误 - {e}")

print(f"\n4. 测试结果:")
print(f"   数据变化次数: {change_count}")
if change_count > 5:
    print("   ✅ 传感器响应正常")
elif change_count > 0:
    print("   ⚠️ 传感器响应微弱")
else:
    print("   ❌ 传感器无响应，可能损坏")

print("\n5. 尝试不同测量模式...")
modes = [
    (0x10, "连续高分辨率"),
    (0x13, "连续低分辨率"),
    (0x20, "一次性高分辨率"),
    (0x23, "一次性低分辨率")
]

for mode_code, mode_name in modes:
    try:
        i2c.writeto(addr, b'\x01')  # Power On
        time.sleep_ms(10)
        i2c.writeto(addr, bytes([mode_code]))
        time.sleep_ms(180)
        
        data = i2c.readfrom(addr, 2)
        raw_value = (data[0] << 8) | data[1]
        lux = raw_value / 1.2
        print(f"   {mode_name}: 原始={raw_value}, 光照={lux:.2f} lux")
    except Exception as e:
        print(f"   {mode_name}: 错误 - {e}")

print("\n=== 调试完成 ===")

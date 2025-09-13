# 最简单的DHT11测试程序
import machine
import time
import json

print("=== 藏红花培育系统 - 简单测试版 ===")

# 初始化LED
led = machine.Pin('C13', machine.Pin.OUT)
led.high()  # 初始熄灭

# 初始化DHT11 - 使用官方DHT驱动
from dht import DHT11
sensor_pin = machine.Pin('A1', machine.Pin.IN, machine.Pin.PULL_UP)
dht11 = DHT11(sensor_pin)

# 初始化I2C总线用于GY-302
i2c = machine.I2C(1, freq=100000)

# GY-302 (BH1750) 光照传感器
class GY302:
    def __init__(self, i2c, addr=0x23):
        self.i2c = i2c
        self.addr = addr
        # 先检查I2C设备是否存在
        try:
            devices = self.i2c.scan()
            print(f"检测到的I2C设备: {[hex(d) for d in devices]}")
            if self.addr not in devices:
                print(f"警告: 地址 {hex(self.addr)} 未找到，尝试地址 0x5C")
                self.addr = 0x5C
                if self.addr not in devices:
                    raise Exception(f"GY-302传感器未找到，可用地址: {[hex(d) for d in devices]}")
        except Exception as e:
            raise Exception(f"I2C扫描失败: {e}")
        
        self.power_on()
        self.reset()
        self.set_mode(0x20)  # 连续高分辨率模式
    
    def power_on(self):
        self.i2c.writeto(self.addr, b'\x01')
    
    def reset(self):
        self.i2c.writeto(self.addr, b'\x07')
    
    def set_mode(self, mode):
        self.i2c.writeto(self.addr, bytes([mode]))
    
    def read_lux(self):
        try:
            # 等待测量完成
            time.sleep_ms(180)  # BH1750需要180ms测量时间
            data = self.i2c.readfrom(self.addr, 2)
            # 检查数据是否有效
            if len(data) == 2:
                raw_value = (data[0] << 8) | data[1]
                if raw_value > 0:
                    lux = raw_value / 1.2
                    print(f"原始数据: {raw_value}, 光照: {lux:.2f} lux")
                    return lux
                else:
                    print("光照传感器返回0值")
                    return None
            else:
                print(f"光照传感器数据长度错误: {len(data)}")
                return None
        except Exception as e:
            print(f"GY-302读取失败: {e}")
            return None

# 初始化GY-302
try:
    gy302 = GY302(i2c)
    print("✅ GY-302光照传感器初始化成功")
except Exception as e:
    print(f"⚠️ GY-302初始化失败: {e}")
    gy302 = None

# 初始化土壤湿度传感器 (ADC)
try:
    soil_adc = machine.ADC(machine.Pin('A2'))
    print("✅ 土壤湿度传感器初始化成功")
except Exception as e:
    print(f"⚠️ 土壤湿度传感器初始化失败: {e}")
    soil_adc = None

print("✅ 初始化完成")
print("开始读取数据...")

cycle = 0
while True:
    try:
        cycle += 1
        
        # 读取温湿度
        dht11.measure()
        temp = dht11.temperature()
        humi = dht11.humidity()
        
        # 读取光照强度
        if gy302:
            lux = gy302.read_lux()
        else:
            lux = None
        
        # 读取土壤湿度
        if soil_adc:
            soil_raw = soil_adc.read_u16()
            # 检测传感器是否真的连接（合理范围检测）
            if 1000 < soil_raw < 50000:  # 合理范围，避免悬空引脚噪声
                # 转换为百分比 (0-100%)
                # 假设：0 = 很湿，65535 = 很干
                soil_percent = max(0, min(100, (65535 - soil_raw) * 100 // 65535))
            else:
                soil_percent = None  # 传感器未连接或数据异常
        else:
            soil_percent = None
        
        # 创建数据包
        data = {
            "cycle": cycle,
            "temp": temp,
            "humi": humi,
            "lux": lux,
            "soil": soil_percent,
            "timestamp": time.ticks_ms()
        }
        
        # 输出JSON
        print(json.dumps(data))
        
        # LED闪烁表示成功
        led.low()
        time.sleep_ms(100)
        led.high()
        
    except Exception as e:
        print(f"错误: {e}")
        # 错误时LED双闪
        for _ in range(2):
            led.low()
            time.sleep_ms(200)
            led.high()
            time.sleep_ms(200)
    
    time.sleep(2)  # 2秒间隔

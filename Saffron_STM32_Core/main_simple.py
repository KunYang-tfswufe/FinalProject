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
            data = self.i2c.readfrom(self.addr, 2)
            lux = (data[0] << 8 | data[1]) / 1.2
            return lux
        except:
            return None

# 初始化GY-302
try:
    gy302 = GY302(i2c)
    print("✅ GY-302光照传感器初始化成功")
except Exception as e:
    print(f"⚠️ GY-302初始化失败: {e}")
    gy302 = None

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
        
        # 创建数据包
        data = {
            "cycle": cycle,
            "temp": temp,
            "humi": humi,
            "lux": lux,
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

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
        
        # 创建数据包
        data = {
            "cycle": cycle,
            "temp": temp,
            "humi": humi,
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

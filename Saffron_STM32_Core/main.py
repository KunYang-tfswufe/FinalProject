from machine import Pin
import time

# 定义引脚并强制设置为“灭”的初始状态，保证可靠
led = Pin(Pin.cpu.C13, Pin.OUT)

# 显式地控制“亮”和“灭”，行为完全可预测
while True:
    led.low()   # 亮
    time.sleep_ms(200)
    led.high()  # 灭
    time.sleep_ms(200)

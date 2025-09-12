# 最终极简代码 (健壮版)
from machine import Pin
import time

led = Pin(Pin.cpu.C13, Pin.OUT)
led.high()  # 关键: 确保初始状态是“灭”

while True:
    led.low()   # 点亮
    time.sleep_ms(500)
    led.high()  # 熄灭
    time.sleep_ms(500)

# /home/imak/FinalProject/Saffron_STM32_Core/main.py
# 版本 3.1 - 在读取传感器时关闭中断以保证时序

from machine import Pin, disable_irq, enable_irq
import dht
import time
import json

# --- 1. 初始化硬件 (已验证 OK) ---
status_led = Pin(Pin.cpu.C13, Pin.OUT)
status_led.high()
sensor_pin = Pin(Pin.cpu.A1, Pin.IN, Pin.PULL_UP)

# --- 2. 创建传感器对象 (已验证 OK) ---
try:
    sensor = dht.DHT11(sensor_pin)
    print("DHT11 sensor initialized successfully.")
    for _ in range(3):
        status_led.low(); time.sleep_ms(50); status_led.high(); time.sleep_ms(50)
except Exception as e:
    print(f"FATAL: Failed to initialize DHT11 sensor: {e}")
    while True:
        status_led.toggle(); time.sleep_ms(100)

# --- 3. 主循环 ---
print("Starting main loop to read sensor data...")

while True:
    temperature = None
    humidity = None
    
    try:
        # ***** 关键改动 *****
        # 在执行精密时序操作前，关闭全局中断
        irq_state = disable_irq()
        
        # 读取传感器
        sensor.measure()
        
        # 操作完成后，立刻恢复中断
        enable_irq(irq_state)
        # ***** 结束改动 *****

        temperature = sensor.temperature()
        humidity = sensor.humidity()
        
        # 增加一个检查，确保我们读到了有效数据
        if isinstance(temperature, int) and isinstance(humidity, int):
            data_packet = { "temp": temperature, "humi": humidity }
            json_string = json.dumps(data_packet)
            print(json_string)
            status_led.toggle()
        else:
            # 如果 measure() 没出错但读出的不是数字，也打印错误
            print("Sensor read invalid data (non-integer).")
        
    except Exception as e:
        # 如果关闭中断后仍然出错，错误信息会在这里被捕获
        # 操作失败后，也要确保中断被恢复！
        enable_irq(irq_state)
        print(f"Error reading sensor: {e}")

    # 循环延时
    time.sleep(3)

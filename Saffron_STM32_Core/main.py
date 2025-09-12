# /home/imak/FinalProject/Saffron_STM32_Core/main.py
# 版本 3.2 - 修正了 WeAct F411 黑药丸的引脚名称

from machine import Pin, disable_irq, enable_irq
import dht
import time
import json

# --- 1. 初始化硬件 (已修正引脚名称) ---
# 根据 WeAct F411 MicroPython 固件的引脚定义，
# 板载蓝色 LED 是 'C13'，DHT11 传感器连接到 'A1'。
try:
    status_led = Pin('C13', Pin.OUT)
    # 初始状态设置为 high()，根据黑药丸的设计，这是熄灭 LED
    status_led.high()
    
    sensor_pin = Pin('A1', Pin.IN, Pin.PULL_UP)
except ValueError as e:
    # 增加一个捕获，如果连引脚定义都错了，就无限快闪报错，提供明确的视觉反馈
    # 理论上现在不会触发了，但保留它是个好习惯。
    led_fallback = Pin('PC13', Pin.OUT) # 尝试备用名称
    while True:
        led_fallback.toggle()
        time.sleep_ms(50)


# --- 2. 创建传感器对象 ---
try:
    sensor = dht.DHT11(sensor_pin)
    print("DHT11 sensor initialized successfully.")
    # 快速闪烁3次，表示传感器对象创建成功
    for _ in range(3):
        status_led.low(); time.sleep_ms(60); status_led.high(); time.sleep_ms(60)
except Exception as e:
    print(f"FATAL: Failed to initialize DHT11 sensor: {e}")
    # 无限慢闪，表示初始化失败
    while True:
        status_led.toggle(); time.sleep_ms(200)

# --- 3. 主循环 ---
print("Starting main loop to read sensor data...")

while True:
    temperature = None
    humidity = None
    
    try:
        # 在执行精密时序操作前，关闭全局中断，防止干扰
        irq_state = disable_irq()
        
        # 读取传感器
        sensor.measure()
        
        # 操作完成后，立刻恢复中断
        enable_irq(irq_state)

        # 获取温湿度值
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        
        # 确保我们读到了有效的整数数据
        if isinstance(temperature, int) and isinstance(humidity, int):
            # 封装为 JSON
            data_packet = { "temp": temperature, "humi": humidity }
            json_string = json.dumps(data_packet)
            
            # 通过串口 (USB VCP) 打印输出
            print(json_string)
            
            # 切换 LED 状态，表示一次成功的数据采集与发送
            status_led.toggle()
        else:
            print(f"Sensor read invalid data. Temp: {temperature}, Humi: {humidity}")
        
    except Exception as e:
        # 如果在 try 块中发生任何错误，打印它
        print(f"Error reading sensor: {e}")
        # 如果关闭了中断但出错了，确保中断被恢复
        # 注意: 这行可能不会执行如果irq_state未定义，但在我们的逻辑中它总是已定义的
        if 'irq_state' in locals():
            enable_irq(irq_state)
            
    # 每3秒重复一次循环
    time.sleep(3)

import machine
import dht
import time

# 直接定义引脚，不使用任何封装
sensor_pin = machine.Pin('PA1', machine.Pin.IN, machine.Pin.PULL_UP)

# 稍等一下，让传感器稳定
time.sleep_ms(2000)

print("Attempting to create sensor object...")
try:
    sensor = dht.DHT11(sensor_pin)
    print("Sensor object created. Now attempting to measure...")
    
    # 手动执行一次最核心的操作
    machine.disable_irq()
    sensor.measure()
    machine.enable_irq()

    # 读取结果
    temp = sensor.temperature()
    humi = sensor.humidity()
    
    print("--- SUCCESS! ---")
    print("Temperature:", temp, "°C")
    print("Humidity:", humi, "%")

except Exception as e:
    print("--- FAILED! ---")
    print("Error:", e)

print("Test finished.")

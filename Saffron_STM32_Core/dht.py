# /Saffron_STM32_Core/dht.py --  请使用这个版本的内容
# MicroPython DHT-11/DHT-22 driver - PURE PYTHON VERSION
# MIT license; Copyright (c) 2016 Damien P. George

import machine
import time

class DHTBase:
    def __init__(self, pin):
        self.pin = pin
        self.buf = bytearray(5)
        # Add a 1-second delay after sensor initialization
        # This can help prevent initial read errors
        time.sleep_ms(1000)

    def measure(self):
        buf = self.buf
        pin = self.pin
        
        # --- Send Start Signal ---
        pin.init(pin.OUT, pin.PULL_DOWN)
        pin.high()
        time.sleep_ms(50)
        pin.low()
        time.sleep_ms(18)

        # --- Wait for Response ---
        pin.init(pin.IN, pin.PULL_UP)
        
        # Use time_pulse_us for precise timing
        # Wait for the pin to go low (end of 80us response)
        if machine.time_pulse_us(pin, 0, 100) < 0:
            raise Exception("DHT sensor timeout waiting for response")

        # Wait for the pin to go high (start of data)
        if machine.time_pulse_us(pin, 1, 100) < 0:
             raise Exception("DHT sensor timeout waiting for data start")
        
        # --- Read Data Bits ---
        for i in range(5):
            for j in range(7, -1, -1):
                # Wait for pin to go low (end of data bit)
                pulse_len = machine.time_pulse_us(pin, 0, 100)
                if pulse_len < 0:
                    raise Exception("DHT sensor timeout reading data")
                
                # A pulse of ~26-28us is a '0', ~70us is a '1'
                if pulse_len > 40:
                    buf[i] = buf[i] | (1 << j)

        # --- Checksum Validation ---
        checksum = (buf[0] + buf[1] + buf[2] + buf[3]) & 0xFF
        if checksum != buf[4]:
            raise Exception("Checksum error")


class DHT11(DHTBase):
    def humidity(self):
        return self.buf[0]

    def temperature(self):
        return self.buf[2]


class DHT22(DHTBase):
    def humidity(self):
        return (self.buf[0] << 8 | self.buf[1]) * 0.1

    def temperature(self):
        t = ((self.buf[2] & 0x7F) << 8 | self.buf[3]) * 0.1
        if self.buf[2] & 0x80:
            t = -t
        return t

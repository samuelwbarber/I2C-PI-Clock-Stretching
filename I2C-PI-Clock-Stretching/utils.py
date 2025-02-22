import RPi.GPIO as GPIO
import time

class VirtualI2C:
    def __init__(self, scl_pin, sda_pin, delay=0.0002):
        self.scl_pin = scl_pin
        self.sda_pin = sda_pin
        self.delay = delay
        GPIO.setup(self.scl_pin, GPIO.OUT)
        GPIO.setup(self.sda_pin, GPIO.OUT)
        self.SCL_high()
        self.SDA_high()

    def SCL_high(self):
        GPIO.setup(self.scl_pin, GPIO.IN)
        start_time = time.time()
        while GPIO.input(self.scl_pin) == 0:
            if time.time() - start_time > 0.01:
                raise RuntimeError("SCL held low (clock stretching timeout)")
            time.sleep(self.delay)
        time.sleep(self.delay)

    def SCL_low(self):
        GPIO.setup(self.scl_pin, GPIO.OUT)
        GPIO.output(self.scl_pin, GPIO.LOW)
        time.sleep(self.delay)

    def SDA_high(self):
        GPIO.setup(self.sda_pin, GPIO.IN)
        time.sleep(self.delay)

    def SDA_low(self):
        GPIO.setup(self.sda_pin, GPIO.OUT)
        GPIO.output(self.sda_pin, GPIO.LOW)
        time.sleep(self.delay)

    def i2c_start(self):
        self.SDA_high()
        self.SCL_high()
        self.SDA_low()
        self.SCL_low()

    def i2c_stop(self):
        self.SDA_low()
        self.SCL_high()
        self.SDA_high()
        time.sleep(self.delay)

    def i2c_write_byte(self, byte):
        for bit in range(7, -1, -1):
            if (byte >> bit) & 0x1:
                self.SDA_high()
            else:
                self.SDA_low()
            self.SCL_high()
            self.SCL_low()
        self.SDA_high()
        self.SCL_high()
        time.sleep(self.delay)
        ack = GPIO.input(self.sda_pin)
        self.SCL_low()
        return ack == 0

    def i2c_read_byte(self, ack=True):
        byte = 0
        self.SDA_high()
        for i in range(8):
            self.SCL_high()
            bit = GPIO.input(self.sda_pin)
            byte = (byte << 1) | bit
            self.SCL_low()
        if ack:
            self.SDA_low()
        else:
            self.SDA_high()
        self.SCL_high()
        self.SCL_low()
        self.SDA_high()
        return byte

class CCS811:
    def __init__(self, i2c, address=0x5A):
        self.i2c = i2c
        self.address = address

    def reset(self):
        self.write_register(0xFF, [0x11, 0xE5, 0x72, 0x8A])
        time.sleep(0.1)

    def start_application(self):
        self.i2c.i2c_start()
        if not self.i2c.i2c_write_byte((self.address << 1) | 0):
            print("No ACK for sensor address during APP_START")
        self.i2c.i2c_write_byte(0xF4)
        time.sleep(0.5)

    def write_register(self, reg, data):
        self.i2c.i2c_start()
        if not self.i2c.i2c_write_byte((self.address << 1) | 0):
            print("No ACK for sensor address during write_register")
        self.i2c.i2c_write_byte(reg)
        if isinstance(data, list):
            for b in data:
                self.i2c.i2c_write_byte(b)
        else:
            self.i2c.i2c_write_byte(data)
        self.i2c.i2c_stop()

    def read_register(self, reg, length):
        self.i2c.i2c_start()
        if not self.i2c.i2c_write_byte((self.address << 1) | 0):
            print("No ACK for sensor address during read_register (write phase)")
        self.i2c.i2c_write_byte(reg)
        self.i2c.i2c_start()
        if not self.i2c.i2c_write_byte((self.address << 1) | 1):
            print("No ACK for sensor address during read_register (read phase)")
        data = [self.i2c.i2c_read_byte(ack=(i < length - 1)) for i in range(length)]
        self.i2c.i2c_stop()
        return data

    def set_measurement_mode(self, mode):
        self.write_register(0x01, mode)

    def read_data(self):
        return self.read_register(0x02, 8)

    def get_status(self):
        return self.read_register(0x00, 1)[0]

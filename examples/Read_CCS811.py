import RPi.GPIO as GPIO
from I2C_PI_Clock_Stretching import VirtualI2C, CCS811

# Setup GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for I2C communication (adjust as needed)
SCL_PIN = 3
SDA_PIN = 2

# Initialize the Virtual I2C bus
i2c = VirtualI2C(scl_pin=SCL_PIN, sda_pin=SDA_PIN)

# Create the CCS811 sensor object
sensor = CCS811(i2c)

# Reset the sensor and start application mode
sensor.reset()
sensor.start_application()

# Read sensor status and data
status = sensor.get_status()
data = sensor.read_data()

print("Sensor Status: 0x{:02X}".format(status))
print("Sensor Data:", data)

# Clean up GPIO settings
GPIO.cleanup()

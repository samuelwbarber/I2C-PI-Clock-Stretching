# I2C-PI-Clock-Stretching

I2C-PI-Clock-Stretching is a Python library built to address the hardware bug with clock stretching on the Raspberry Pi. It provides a virtual I²C bus implementation via bit-banging, ensuring reliable communication even when devices hold the clock line low. Written for the CCS811 sensor but should work for any I2C device that uses clock stretching.

## Features

- **Virtual I²C Bus:** Implements bit-banged I²C that properly handles clock stretching.
- **CCS811 Sensor Support:** Easily control and communicate with the CCS811 sensor.
- **Robust Communication:** Overcomes the Raspberry Pi's hardware limitations with clock stretching.

## Installation

Install the library via pip:

```bash
pip install I2C-PI-Clock-Stretching==0.1

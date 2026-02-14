# /// script
# requires-python = ">=3.9"
# dependencies = ["adafruit-circuitpython-ahtx0", "adafruit-blinka"]
# ///
"""Test du capteur AHT20 via STEMMA QT/I2C."""

import board
import adafruit_ahtx0

i2c = board.I2C()
sensor = adafruit_ahtx0.AHTx0(i2c)

print(f"Temperature: {sensor.temperature:.1f} C")
print(f"Humidite: {sensor.relative_humidity:.1f} %")

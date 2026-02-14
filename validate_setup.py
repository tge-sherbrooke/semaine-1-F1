# /// script
# requires-python = ">=3.9"
# dependencies = ["adafruit-circuitpython-ahtx0", "adafruit-circuitpython-seesaw", "adafruit-blinka"]
# ///
"""Validation complete de la configuration Raspberry Pi."""

import sys

def test_i2c():
    """Test de la communication I2C."""
    try:
        import board
        i2c = board.I2C()
        print("+ I2C OK")
        return i2c
    except Exception as e:
        print(f"x I2C ERREUR: {e}")
        return None

def test_aht20(i2c):
    """Test du capteur AHT20."""
    try:
        import adafruit_ahtx0
        sensor = adafruit_ahtx0.AHTx0(i2c)
        temp = sensor.temperature
        humidity = sensor.relative_humidity
        print(f"+ AHT20 OK - Temperature: {temp:.1f}C, Humidite: {humidity:.1f}%")
        return True
    except Exception as e:
        print(f"x AHT20 ERREUR: {e}")
        return False

def test_neoslider(i2c):
    """Test du NeoSlider - LEDs."""
    try:
        from adafruit_seesaw.seesaw import Seesaw
        from adafruit_seesaw import neopixel

        neoslider = Seesaw(i2c, addr=0x30)
        pixels = neopixel.NeoPixel(neoslider, 14, 4, pixel_order=neopixel.GRB)

        # Test: allumer en vert
        pixels.fill((0, 255, 0))
        print("+ NeoSlider LEDs OK - LEDs allumees en vert")
        return True, pixels
    except Exception as e:
        print(f"x NeoSlider ERREUR: {e}")
        return False, None

if __name__ == "__main__":
    print("=" * 50)
    print("VALIDATION RASPBERRY PI")
    print("=" * 50)

    i2c = test_i2c()
    if not i2c:
        sys.exit(1)

    aht_ok = test_aht20(i2c)
    neo_ok, pixels = test_neoslider(i2c)

    # Eteindre les LEDs avant de terminer
    if pixels:
        try:
            pixels.fill((0, 0, 0))
        except:
            pass

    print("=" * 50)
    if aht_ok and neo_ok:
        print("+ TOUS LES TESTS REUSSIS")
    else:
        print("x CERTAINS TESTS ONT ECHOUE")
        sys.exit(1)

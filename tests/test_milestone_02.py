"""
Milestone 2: Basic Functionality (35 points)
=============================================

This milestone verifies that the student has:
1. Implemented AHT20 sensor reading logic
2. Used I2C communication correctly
3. Created proper temperature/humidity reading functions

These tests analyze code structure - actual hardware testing
is done locally via validate_pi.py.
"""

import os
import ast
import re
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Helper: Get repository root
# ---------------------------------------------------------------------------
def get_repo_root():
    """Find the repository root by looking for .github folder."""
    current = Path(__file__).parent.parent
    if (current / ".github").exists():
        return current
    return current


REPO_ROOT = get_repo_root()


# ---------------------------------------------------------------------------
# Test 2.1: I2C Initialization (10 points)
# ---------------------------------------------------------------------------
def test_i2c_initialization():
    """
    Verify that the script initializes I2C communication.

    Expected: Code that creates an I2C bus using board.I2C()

    Suggestion: Initialize I2C with:
        i2c = board.I2C()
    """
    script_path = REPO_ROOT / "test_aht20.py"

    if not script_path.exists():
        pytest.skip("test_aht20.py not found")

    content = script_path.read_text()

    # Check for I2C initialization patterns
    has_i2c = any([
        "board.I2C()" in content,
        "busio.I2C" in content,
        "board.SCL" in content,
    ])

    if not has_i2c:
        pytest.fail(
            f"\n\n"
            f"Expected: I2C bus initialization\n"
            f"Actual: No I2C initialization found\n\n"
            f"Suggestion: Add I2C initialization in your code:\n"
            f"  import board\n"
            f"  i2c = board.I2C()  # Uses board.SCL and board.SDA\n"
            f"\n"
            f"The AHT20 communicates via I2C protocol.\n"
        )


# ---------------------------------------------------------------------------
# Test 2.2: AHT20 Sensor Object Creation (10 points)
# ---------------------------------------------------------------------------
def test_aht20_sensor_creation():
    """
    Verify that the script creates an AHT20 sensor object.

    Expected: AHTx0 sensor initialization

    Suggestion: Create sensor with:
        sensor = adafruit_ahtx0.AHTx0(i2c)
    """
    script_path = REPO_ROOT / "test_aht20.py"

    if not script_path.exists():
        pytest.skip("test_aht20.py not found")

    content = script_path.read_text()

    # Check for sensor creation patterns
    has_sensor = any([
        "AHTx0(" in content,
        "adafruit_ahtx0." in content and "i2c" in content.lower(),
    ])

    if not has_sensor:
        pytest.fail(
            f"\n\n"
            f"Expected: AHT20 sensor object creation\n"
            f"Actual: No AHT20 sensor initialization found\n\n"
            f"Suggestion: Create the sensor object:\n"
            f"  import adafruit_ahtx0\n"
            f"  sensor = adafruit_ahtx0.AHTx0(i2c)\n"
        )


# ---------------------------------------------------------------------------
# Test 2.3: Temperature Reading (7 points)
# ---------------------------------------------------------------------------
def test_temperature_reading():
    """
    Verify that the script reads temperature from the sensor.

    Expected: Code that accesses sensor.temperature

    Suggestion: Read temperature with:
        temp = sensor.temperature
        print(f"Temperature: {temp:.1f} C")
    """
    script_path = REPO_ROOT / "test_aht20.py"

    if not script_path.exists():
        pytest.skip("test_aht20.py not found")

    content = script_path.read_text()

    has_temp = any([
        ".temperature" in content,
        "temperature" in content.lower() and "sensor" in content.lower(),
    ])

    if not has_temp:
        pytest.fail(
            f"\n\n"
            f"Expected: Temperature reading from sensor\n"
            f"Actual: No temperature reading found\n\n"
            f"Suggestion: Read temperature like this:\n"
            f"  temperature = sensor.temperature\n"
            f"  print(f\"Temperature: {{temperature:.1f}} C\")\n"
        )


# ---------------------------------------------------------------------------
# Test 2.4: Humidity Reading (8 points)
# ---------------------------------------------------------------------------
def test_humidity_reading():
    """
    Verify that the script reads humidity from the sensor.

    Expected: Code that accesses sensor.relative_humidity

    Suggestion: Read humidity with:
        humidity = sensor.relative_humidity
        print(f"Humidite: {humidity:.1f} %")
    """
    script_path = REPO_ROOT / "test_aht20.py"

    if not script_path.exists():
        pytest.skip("test_aht20.py not found")

    content = script_path.read_text()

    has_humidity = any([
        ".relative_humidity" in content,
        "humidity" in content.lower() and "sensor" in content.lower(),
    ])

    if not has_humidity:
        pytest.fail(
            f"\n\n"
            f"Expected: Humidity reading from sensor\n"
            f"Actual: No humidity reading found\n\n"
            f"Suggestion: Read humidity like this:\n"
            f"  humidity = sensor.relative_humidity\n"
            f"  print(f\"Humidite: {{humidity:.1f}} %\")\n"
            f"\n"
            f"The AHT20 measures relative humidity as a percentage.\n"
        )


# ---------------------------------------------------------------------------
# Test 2.5: Hardware Validation Passed (Bonus for early tests)
# ---------------------------------------------------------------------------
def test_hardware_markers_present():
    """
    Verify that hardware validation markers exist.

    Expected: Marker files from validate_pi.py execution

    Suggestion: Run validate_pi.py on your Raspberry Pi and push results.
    """
    markers_dir = REPO_ROOT / ".test_markers"

    if not markers_dir.exists():
        pytest.skip("No .test_markers/ directory - skipping hardware check")

    # Look for AHT20-specific markers
    aht_markers = list(markers_dir.glob("*aht*")) + list(markers_dir.glob("*i2c*"))

    # Also check the general test summary
    summary = markers_dir / "test_summary.txt"

    if summary.exists():
        content = summary.read_text().lower()
        if "aht20" in content or "i2c" in content:
            return  # Pass - hardware was validated

    if not aht_markers:
        pytest.fail(
            f"\n\n"
            f"Expected: AHT20/I2C hardware validation markers\n"
            f"Actual: No hardware-specific markers found\n\n"
            f"Suggestion: On your Raspberry Pi:\n"
            f"  1. Connect the AHT20 sensor via STEMMA QT\n"
            f"  2. Run: sudo i2cdetect -y 1\n"
            f"  3. Verify address 0x38 appears\n"
            f"  4. Run: python3 validate_pi.py\n"
            f"  5. Commit and push .test_markers/\n"
        )

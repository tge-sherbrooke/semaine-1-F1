# /// script
# requires-python = ">=3.9"
# dependencies = ["adafruit-circuitpython-ahtx0", "adafruit-circuitpython-seesaw", "adafruit-blinka"]
# ///
"""
Local Hardware Validation for Formatif F1
==========================================

Run this script ON YOUR RASPBERRY PI to validate hardware setup.
It creates marker files that GitHub Actions will verify.

Usage:
    python3 validate_pi.py

The script will:
1. Check SSH key configuration
2. Verify I2C communication
3. Test AHT20 sensor
4. Test NeoSlider (optional)
5. Create marker files for GitHub Actions

After running successfully, commit and push the .test_markers/ folder.
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime


# ---------------------------------------------------------------------------
# Terminal Colors
# ---------------------------------------------------------------------------
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def success(msg):
    print(f"{Colors.GREEN}[PASS] {msg}{Colors.END}")


def fail(msg):
    print(f"{Colors.RED}[FAIL] {msg}{Colors.END}")


def warn(msg):
    print(f"{Colors.YELLOW}[WARN] {msg}{Colors.END}")


def info(msg):
    print(f"{Colors.BLUE}[INFO] {msg}{Colors.END}")


def header(msg):
    print(f"\n{Colors.BOLD}{'='*60}")
    print(f" {msg}")
    print(f"{'='*60}{Colors.END}\n")


# ---------------------------------------------------------------------------
# Marker Management
# ---------------------------------------------------------------------------
MARKERS_DIR = Path(__file__).parent / ".test_markers"


def create_marker(name, content):
    """Create a marker file for GitHub Actions verification."""
    MARKERS_DIR.mkdir(exist_ok=True)
    marker_path = MARKERS_DIR / f"{name}.txt"
    timestamp = datetime.now().isoformat()
    marker_path.write_text(f"Verified: {timestamp}\n{content}\n")
    info(f"Marker created: {marker_path.name}")


# ---------------------------------------------------------------------------
# Test: SSH Key
# ---------------------------------------------------------------------------
def check_ssh_key():
    """Verify SSH key exists and GitHub connection works."""
    header("SSH KEY VERIFICATION")

    ssh_dir = Path.home() / ".ssh"
    key_files = [
        "id_ed25519_iot.pub",  # Recommended for this course
        "id_ed25519.pub",
        "id_rsa.pub",
    ]

    key_found = None
    for key_name in key_files:
        key_path = ssh_dir / key_name
        if key_path.exists():
            key_found = key_path
            break

    if not key_found:
        fail("No SSH public key found")
        print("\n  To generate an SSH key:")
        print("    ssh-keygen -t ed25519 -C 'iot-cegep' -f ~/.ssh/id_ed25519_iot")
        print("\n  Then add to GitHub:")
        print("    cat ~/.ssh/id_ed25519_iot.pub")
        print("    Copy and paste to: GitHub > Settings > SSH and GPG keys")
        return False

    success(f"SSH key found: {key_found.name}")

    # Test GitHub connection
    try:
        result = subprocess.run(
            ['ssh', '-T', 'git@github.com'],
            capture_output=True, text=True, timeout=10
        )
        if 'successfully authenticated' in result.stderr.lower():
            success("GitHub SSH connection works")
            create_marker("ssh_key_verified", f"Key: {key_found.name}")
            return True
        else:
            warn("GitHub connection uncertain - key may not be added")
            create_marker("ssh_key_verified", f"Key: {key_found.name} (unverified)")
            return True
    except Exception as e:
        warn(f"Could not test GitHub connection: {e}")
        create_marker("ssh_key_verified", f"Key: {key_found.name} (connection not tested)")
        return True


# ---------------------------------------------------------------------------
# Test: I2C Communication
# ---------------------------------------------------------------------------
def check_i2c():
    """Verify I2C is enabled and working."""
    header("I2C COMMUNICATION")

    try:
        import board
        i2c = board.I2C()
        success("I2C bus initialized")
        return i2c
    except Exception as e:
        fail(f"I2C initialization failed: {e}")
        print("\n  Enable I2C on Raspberry Pi:")
        print("    sudo raspi-config > Interface Options > I2C > Enable")
        print("    sudo reboot")
        return None


# ---------------------------------------------------------------------------
# Test: AHT20 Sensor
# ---------------------------------------------------------------------------
def check_aht20(i2c):
    """Test AHT20 sensor reading."""
    header("AHT20 SENSOR TEST")

    if i2c is None:
        fail("Cannot test AHT20 - I2C not available")
        return False

    try:
        import adafruit_ahtx0

        sensor = adafruit_ahtx0.AHTx0(i2c)
        info("AHT20 found at address 0x38")

        # Read values
        temp = sensor.temperature
        humidity = sensor.relative_humidity

        # Sanity checks
        assert -40 <= temp <= 85, f"Temperature out of range: {temp}"
        assert 0 <= humidity <= 100, f"Humidity out of range: {humidity}"

        success(f"Temperature: {temp:.1f} C")
        success(f"Humidity: {humidity:.1f} %")

        create_marker("aht20_verified", f"T={temp:.1f}C H={humidity:.1f}%")
        return True

    except ImportError:
        fail("adafruit_ahtx0 not installed")
        print("\n  Install with:")
        print("    pip install adafruit-circuitpython-ahtx0")
        return False
    except AssertionError as e:
        fail(f"AHT20 sanity check failed: {e}")
        return False
    except Exception as e:
        fail(f"AHT20 error: {e}")
        print("\n  Check connections:")
        print("    - STEMMA QT SHIM pressed onto GPIO header")
        print("    - STEMMA QT cable clicked into SHIM and AHT20")
        print("\n  Run i2cdetect to verify:")
        print("    sudo i2cdetect -y 1")
        return False


# ---------------------------------------------------------------------------
# Test: NeoSlider (Optional)
# ---------------------------------------------------------------------------
def check_neoslider(i2c):
    """Test NeoSlider (optional component)."""
    header("NEOSLIDER TEST (Optional)")

    if i2c is None:
        warn("Cannot test NeoSlider - I2C not available")
        return True  # Optional, don't fail

    try:
        from adafruit_seesaw.seesaw import Seesaw
        from adafruit_seesaw import neopixel

        neoslider = Seesaw(i2c, addr=0x30)
        pixels = neopixel.NeoPixel(neoslider, 14, 4, pixel_order=neopixel.GRB)

        # Flash green briefly
        pixels.fill((0, 255, 0))
        import time
        time.sleep(0.5)
        pixels.fill((0, 0, 0))

        success("NeoSlider LEDs working")
        create_marker("neoslider_verified", "LEDs tested successfully")
        return True

    except ImportError:
        warn("NeoSlider libraries not installed (optional)")
        return True
    except Exception as e:
        warn(f"NeoSlider not detected: {e}")
        info("NeoSlider is optional - this doesn't affect your grade")
        return True


# ---------------------------------------------------------------------------
# Test: Script Validation
# ---------------------------------------------------------------------------
def check_aht20_script():
    """Verify test_aht20.py script."""
    header("SCRIPT VALIDATION")

    script_path = Path(__file__).parent / "test_aht20.py"

    if not script_path.exists():
        fail("test_aht20.py not found")
        print("\n  Create your test_aht20.py script in the same folder.")
        return False

    success("test_aht20.py exists")

    # Check syntax
    try:
        with open(script_path) as f:
            compile(f.read(), script_path, 'exec')
        success("Python syntax is valid")
    except SyntaxError as e:
        fail(f"Syntax error on line {e.lineno}: {e.msg}")
        return False

    # Check required content
    content = script_path.read_text()
    checks = [
        ("import board", "board import"),
        ("adafruit_ahtx0", "adafruit_ahtx0 import"),
    ]

    all_present = True
    for pattern, desc in checks:
        if pattern in content:
            success(f"Found: {desc}")
        else:
            fail(f"Missing: {desc}")
            all_present = False

    if all_present:
        create_marker("aht20_script_verified", "Script structure valid")

    return all_present


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print(f"\n{Colors.BOLD}Formatif F1 - Local Hardware Validation{Colors.END}")
    print(f"{'='*60}\n")

    results = {}

    # Run all checks
    results["SSH"] = check_ssh_key()
    i2c = check_i2c()
    results["I2C"] = i2c is not None
    results["AHT20"] = check_aht20(i2c)
    results["NeoSlider"] = check_neoslider(i2c)
    results["Script"] = check_aht20_script()

    # Summary
    header("FINAL RESULTS")

    all_required_passed = results["SSH"] and results["I2C"] and results["AHT20"] and results["Script"]

    for test, passed in results.items():
        if passed:
            success(f"{test}: OK")
        elif test == "NeoSlider":
            warn(f"{test}: SKIPPED (optional)")
        else:
            fail(f"{test}: FAILED")

    print()

    if all_required_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}")
        print("=" * 60)
        print(" ALL REQUIRED TESTS PASSED!")
        print("=" * 60)
        print(f"{Colors.END}")

        create_marker("all_tests_passed", "All required validations completed")

        print("\nNext steps:")
        print("  git add .test_markers/")
        print("  git commit -m \"feat: validation locale completee\"")
        print("  git push")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}")
        print("=" * 60)
        print(" SOME TESTS FAILED - Fix issues and run again")
        print("=" * 60)
        print(f"{Colors.END}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

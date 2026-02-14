#!/bin/bash
# Script de validation pour le Formatif F1 sur Raspberry Pi
# Executez: bash validate_pi.sh

echo "========================================"
echo "VALIDATION FORMATIF F1 - Raspberry Pi"
echo "========================================"
echo ""

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Compteur
passed=0
failed=0

# Fonction pour verifier une commande
check() {
    local name="$1"
    local command="$2"

    echo -n "Checking $name... "
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}+ PASS${NC}"
        ((passed++))
        return 0
    else
        echo -e "${RED}x FAIL${NC}"
        ((failed++))
        return 1
    fi
}

# 1. Verifier Python 3
check "Python 3 installed" "which python3"

# 2. Verifier pip
check "pip3 installed" "which pip3"

# 3. Verifier I2C tools
check "i2c-tools installed" "which i2cdetect"

# 4. Verifier que I2C est active
echo -n "Checking I2C enabled... "
if i2cdetect -y 1 > /dev/null 2>&1 || [ -e /dev/i2c-1 ]; then
    echo -e "${GREEN}+ PASS${NC}"
    ((passed++))
else
    echo -e "${RED}x FAIL${NC} (Run: sudo raspi-config -> Interface -> I2C)"
    ((failed++))
fi

# 5. Verifier les bibliotheques Python
echo ""
echo "Checking Python libraries..."
check "adafruit_ahtx0 installed" "python3 -c 'import adafruit_ahtx0'"
check "board module installed" "python3 -c 'import board'"

# 6. Scanner le bus I2C
echo ""
echo "Scanning I2C bus for AHT20..."
if i2cdetect -y 1 2>/dev/null | grep -q "38"; then
    echo -e "${GREEN}+ AHT20 detected at 0x38${NC}"
    ((passed++))
else
    echo -e "${RED}x No AHT20 found at 0x38${NC}"
    echo "  Check wiring:"
    echo "  - STEMMA QT SHIM pressed onto GPIO header"
    echo "  - STEMMA QT cable clicked into SHIM and AHT20"
    ((failed++))
fi

# 7. Verifier le script capteur.py
echo ""
if [ -f "capteur.py" ]; then
    echo -e "${GREEN}+ capteur.py exists${NC}"
    ((passed++))

    echo -n "Testing capteur.py execution... "
    if timeout 10 python3 capteur.py > /dev/null 2>&1; then
        echo -e "${GREEN}+ PASS${NC}"
        ((passed++))

        echo ""
        echo "Sample output:"
        echo "----------------------------------------"
        python3 capteur.py
        echo "----------------------------------------"
    else
        echo -e "${RED}x FAIL${NC} (Script has errors)"
        ((failed++))
    fi
else
    echo -e "${YELLOW}capteur.py not found${NC}"
    echo "  Create it with the code from README.md"
    ((failed++))
fi

# Resume
echo ""
echo "========================================"
echo "RESUME DE LA VALIDATION"
echo "========================================"
echo -e "${GREEN}Passed: $passed${NC}"
echo -e "${RED}Failed: $failed${NC}"
echo ""

if [ $failed -eq 0 ]; then
    echo -e "${GREEN}Tout fonctionne! Vous pouvez pousser votre code.${NC}"
    exit 0
else
    echo -e "${RED}Corrigez les erreurs avant de continuer.${NC}"
    exit 1
fi

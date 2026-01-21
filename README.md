# Formatif F1 — Introduction au Raspberry Pi et capteurs Adafruit

**Cours** : 243-413-SH — Introduction aux objets connectés
**Semaine** : 1
**Type** : Formative (non notée)
**Date limite** : Fin de la séance de laboratoire

---

## Objectif

Ce formatif vise à vérifier que vous êtes capable de :
1. ✅ Configurer SSH sans mot de passe (depuis Windows)
2. ✅ Installer UV et gérer les dépendances Python
3. ✅ Détecter un capteur I²C avec `i2cdetect`
4. ✅ Lire un capteur BMP280 (température, pression, altitude)
5. ✅ Contrôler un NeoSlider (potentiomètre + LEDs)

---

## Instructions

### Étape 1 : Connexion SSH sans mot de passe (Windows PowerShell)

#### Générer une clé SSH

```powershell
ssh-keygen -t ed25519 -C "mon-raspberry-pi"
```

- Appuyez **Entrée** pour accepter l'emplacement par défaut
- Appuyez **Entrée** deux fois pour laisser le mot de passe vide

#### Copier la clé sur le Raspberry Pi

```powershell
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh utilisateur@HOSTNAME.local "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

> ⚠️ Remplacez `HOSTNAME` par le nom de votre Raspberry Pi et `utilisateur` par votre nom d'utilisateur.

#### Tester la connexion

```powershell
ssh utilisateur@HOSTNAME.local
```

Vous devriez vous connecter **sans entrer de mot de passe**.

---

### Étape 2 : Installer UV

Une fois connecté en SSH sur le Raspberry Pi :

```bash
# Installer UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Recharger le shell
source ~/.bashrc

# Vérifier l'installation
uv --version
```

---

### Étape 3 : Activer I2C et vérifier les capteurs

```bash
# Activer I2C
sudo raspi-config nonint do_i2c 0

# Installer les outils I2C
sudo apt update && sudo apt install -y i2c-tools

# Scanner le bus I2C
sudo i2cdetect -y 1
```

Vous devriez voir :
- `77` pour le BMP280
- `30` pour le NeoSlider

⚠️ **IMPORTANT** : Les capteurs fonctionnent UNIQUEMENT en 3.3V !

---

### Étape 4 : Tester le capteur BMP280

Créez le fichier `test_bmp280.py` :

```python
# /// script
# requires-python = ">=3.9"
# dependencies = ["adafruit-circuitpython-bmp280", "adafruit-blinka"]
# ///
"""Test du capteur BMP280 via STEMMA QT/I2C."""

import board
import adafruit_bmp280

i2c = board.I2C()
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x77)

print(f"Température: {sensor.temperature:.1f} °C")
print(f"Pression: {sensor.pressure:.1f} hPa")
print(f"Altitude: {sensor.altitude:.1f} m")
```

Exécutez :

```bash
uv run test_bmp280.py
```

---

### Étape 5 : Tester le NeoSlider

Créez le fichier `test_neoslider.py` :

```python
# /// script
# requires-python = ">=3.9"
# dependencies = ["adafruit-circuitpython-seesaw", "adafruit-blinka"]
# ///
"""Test du NeoSlider - Animation arc-en-ciel sur les LEDs."""

import board
import time
from rainbowio import colorwheel
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw import neopixel

# Configuration NeoSlider
i2c = board.I2C()
neoslider = Seesaw(i2c, 0x30)
pixels = neopixel.NeoPixel(neoslider, 14, 4, pixel_order=neopixel.GRB)

# Position dans la roue des couleurs
color_pos = 0

while True:
    # Remplir les pixels avec la couleur actuelle
    pixels.fill(colorwheel(color_pos))
    
    # Avancer vers la couleur suivante
    color_pos = (color_pos + 1) % 256
    
    time.sleep(0.02)
```

Exécutez :

```bash
uv run test_neoslider.py
```

**Validation** : Les 4 LEDs affichent une animation arc-en-ciel. Appuyez `Ctrl+C` pour arrêter.

---

## Câblage STEMMA QT

| Fil | Raspberry Pi |
|-----|--------------|
| Rouge (VIN) | 3.3V |
| Noir (GND) | GND |
| Bleu (SDA) | GPIO 2 |
| Jaune (SCL) | GPIO 3 |

⚠️ **VIN doit être connecté à 3.3V, PAS 5V !**

---

## Validation automatique

### 1. Validation GitHub Actions (CI)

Les tests GitHub Actions vérifient **la structure du code** sans nécessiter de matériel :

```bash
# Les tests s'exécutent automatiquement quand vous poussez sur GitHub
# Ils utilisent des mocks pour simuler le matériel
```

**Ce qui est testé en CI :**
- ✅ Présence de `requirements.txt` avec les bonnes dépendances
- ✅ Syntaxe Python valide
- ✅ Structure du script (imports, création du capteur, etc.)

### 2. Validation sur le Raspberry Pi

Pour valider le **fonctionnement matériel** sur le Raspberry Pi :

```bash
uv run validate_setup.py
# ou
bash validate_pi.sh
```

---

## Livrables

Dans ce dépôt, vous devez avoir :

- [ ] `test_bmp280.py` — Script de lecture du capteur BMP280
- [ ] `test_neoslider.py` — Script de test du NeoSlider
- [ ] `captures/` — Captures d'écran (optionnel)

---

## Résumé des commandes

```bash
# Sur Windows PowerShell (avant connexion)
ssh-keygen -t ed25519 -C "mon-raspberry-pi"
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh utilisateur@HOSTNAME.local "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
ssh utilisateur@HOSTNAME.local

# Sur le Raspberry Pi
curl -LsSf https://astral.sh/uv/install.sh | sh && source ~/.bashrc
sudo apt install -y i2c-tools
sudo raspi-config nonint do_i2c 0
sudo i2cdetect -y 1
uv run test_bmp280.py
uv run test_neoslider.py
```

---

## Ressources

- [Guide de configuration LLM](guide-configuration-rpi.md)
- [Guide étudiant](guide-etudiant-rpi.md)

---

Bonne chance ! 🚀

# Formatif F1 — Introduction au Raspberry Pi et capteurs Adafruit

**Cours** : 243-413-SH — Introduction aux objets connectes
**Semaine** : 1
**Type** : Formative (non notee)
**Retries** : Illimites - poussez autant de fois que necessaire!

---

> **Pratique autonome** -- Ce formatif est une evaluation formative (non notee). Contrairement au laboratoire guide, vous devez completer les taches de maniere autonome. Les tests automatiques vous donnent une retroaction immediate a chaque push.

## Ce que vous avez appris en labo

Le laboratoire de la semaine 1 vous a guide a travers :

- Connexion SSH au Raspberry Pi depuis votre poste Windows
- Detection de peripheriques I2C avec `i2cdetect`
- Lecture du capteur AHT20 (temperature et humidite)
- Execution de scripts Python avec `uv run`

Ce formatif vous demande d'appliquer ces competences de maniere autonome.

---

## Progressive Milestones

Ce formatif utilise des **jalons progressifs** avec retroaction detaillee:

| Jalon | Points | Verification |
|-------|--------|-------------|
| **Milestone 1** | 25 pts | Script existe, syntaxe valide, tests locaux executes |
| **Milestone 2** | 35 pts | I2C initialise, capteur AHT20 cree, lecture temperature/humidite |
| **Milestone 3** | 40 pts | Fonction main(), gestion d'erreurs, qualite du code |

**Chaque test echoue vous dit**:
- Ce qui etait attendu
- Ce qui a ete trouve
- Une suggestion pour corriger

---

## Objectif

Ce formatif vise a verifier que vous etes capable de :
1. Configurer Git et SSH sur le Raspberry Pi (via `gh auth login`)
2. Installer UV et gerer les dependances Python
3. Detecter un capteur I2C avec `i2cdetect`
4. Lire un capteur AHT20 (temperature, humidite)
5. Controler un NeoSlider (potentiometre + LEDs) - optionnel

---

## Workflow de soumission

```
+-----------------------------------------------------------------+
|                    WORKLOAD FORMATIF F1                          |
+-----------------------------------------------------------------+
|                                                                  |
|  1. Sur le Raspberry Pi (Git et SSH deja configures en labo)     |
|     +-- Installer UV                                             |
|     +-- Cloner votre depot GitHub (avec URL SSH)                 |
|     +-- Creer test_aht20.py                                     |
|     +-- Executer: python3 run_tests.py                           |
|     +-- Corriger les erreurs                                     |
|     +-- Pousser: git add, commit, push                           |
|                                                                  |
|  2. GitHub Actions valide automatiquement                        |
|     +-- Verifie les marqueurs de tests                           |
|     +-- Confirme que vous avez tout complete                     |
|                                                                  |
+-----------------------------------------------------------------+
```

---

## Instructions detaillees

### Etape 1 : Configuration Git et SSH

Vous avez deja configure Git et SSH dans le labo (via `gh auth login`).
Si ce n'est pas fait, consultez la procedure du labo semaine 1.

---

### Etape 2 : Installer UV et cloner le depot

```bash
# Installer UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Recharger le shell
source ~/.bashrc
```

```bash
# Cloner votre depot GitHub Classroom avec l'URL SSH
git clone git@github.com:tge-sherbrooke/semaine-1-f1-votre-username.git
cd semaine-1-f1-votre-username
```

> **Note** : Utilisez l'URL **SSH** affichee sur GitHub (commence par `git@github.com:`)

---

### Etape 3 : Activer I2C et verifier les capteurs

```bash
# Activer I2C
sudo raspi-config nonint do_i2c 0

# Installer les outils I2C
sudo apt update && sudo apt install -y i2c-tools

# Scanner le bus I2C
sudo i2cdetect -y 1
```

Vous devriez voir :
- `38` pour le AHT20
- `30` pour le NeoSlider

**IMPORTANT** : Les capteurs fonctionnent UNIQUEMENT en 3.3V !

---

### Etape 4 : Creer et tester le AHT20

Creez le fichier `test_aht20.py` :

```python
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
```

Testez-le :

```bash
uv run test_aht20.py
```

---

### Etape 5 : Creer et tester le NeoSlider (optionnel)

Creez le fichier `test_neoslider.py` :

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
    pixels.fill(colorwheel(color_pos))
    color_pos = (color_pos + 1) % 256
    time.sleep(0.02)
```

Testez-le :

```bash
uv run test_neoslider.py
```

---

### Etape 6 : Executer les tests locaux

**Ceci est l'etape obligatoire avant de pousser!**

```bash
python3 run_tests.py
```

Le script `run_tests.py` va :
1. Verifier la connexion SSH avec GitHub
2. Verifier que `test_aht20.py` est correct
3. Verifier que `test_neoslider.py` est correct (optionnel)
4. Scanner le bus I2C pour detecter les capteurs
5. Creer des fichiers marqueurs dans `.test_markers/`

Si tous les tests passent, vous verrez :
```
TOUS LES TESTS SONT PASSES!
```

---

### Etape 7 : Pousser votre travail

Une fois les tests passes :

```bash
git add .
git commit -m "feat: tests AHT20 et NeoSlider completes"
git push
```

GitHub Actions validera automatiquement que vous avez execute les tests.

---

## Cablage STEMMA QT

| Fil | Raspberry Pi |
|-----|--------------|
| Rouge (VIN) | 3.3V |
| Noir (GND) | GND |
| Bleu (SDA) | GPIO 2 |
| Jaune (SCL) | GPIO 3 |

**VIN doit etre connecte a 3.3V, PAS 5V !**

---

## Comprendre la validation

### Pourquoi executer `run_tests.py` AVANT de pousser ?

Le formatif F1 utilise une validation en deux temps :

| Etape | Ou | Ce qui est valide |
|-------|----|-------------------|
| **run_tests.py** | Sur Raspberry Pi | - Connexion GitHub fonctionnelle<br>- Scripts crees<br>- Capteurs detectes |
| **GitHub Actions** | Automatique apres push | - Les marqueurs existent<br>- Syntaxe Python valide |

Cette approche garantit que vous avez **reellement** travaille sur le materiel tout en beneficiant de l'automatisation GitHub.

### Que se passe-t-il si je pousse sans executer les tests ?

GitHub Actions affichera une erreur :
```
ERREUR: Les tests locaux n'ont pas ete executes!
```

Vous devrez alors executer `python3 run_tests.py` sur le Raspberry Pi et repousser.

---

## Livrables

Dans ce depot, vous devez avoir :

- [ ] `test_aht20.py` -- Script de lecture du capteur AHT20
- [ ] `test_neoslider.py` -- Script de test du NeoSlider (optionnel)
- [ ] `.test_markers/` -- Dossier cree par `run_tests.py` (ne pas editer manuellement!)

---

## Resume des commandes

```bash
# ===== SUR RASPBERRY PI (Git et SSH deja configures en labo) =====
ssh utilisateur@HOSTNAME.local

# ===== INSTALLER UV =====
curl -LsSf https://astral.sh/uv/install.sh | sh && source ~/.bashrc

# ===== CLONER LE DEPOT (AVEC URL SSH) =====
git clone git@github.com:tge-sherbrooke/semaine-1-f1-votre-username.git
cd semaine-1-f1-votre-username

# ===== ACTIVER I2C =====
sudo raspi-config nonint do_i2c 0
sudo apt install -y i2c-tools

# ===== SCANNER I2C =====
sudo i2cdetect -y 1

# ===== TESTER LES CAPTEURS =====
uv run test_aht20.py
uv run test_neoslider.py

# ===== EXECUTER LES TESTS =====
python3 run_tests.py

# ===== POUSSER =====
git add .
git commit -m "feat: tests completes"
git push
```

---

## Ressources

- [Guide de l'etudiant](../deliverables/activites/semaine-1/labo/guide-etudiant.md)
- [Guide de depannage](../deliverables/activites/semaine-1/labo/guide-depannage.md)

---

Bonne chance !

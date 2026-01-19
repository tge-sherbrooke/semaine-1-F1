# Formatif F1 — Introduction au Raspberry Pi et BMP280

**Cours** : 243-413-SH — Introduction aux objets connectés
**Semaine** : 1
**Type** : Formative (non notée)
**Date limite** : Fin de la séance de laboratoire

---

## Objectif

Ce formatif vise à vérifier que vous êtes capable de :
1. ✅ Utiliser SSH pour vous connecter au Raspberry Pi (depuis Windows)
2. ✅ Installer les bibliothèques Python nécessaires (BMP280)
3. ✅ Détecter un capteur I²C avec `i2cdetect`
4. ✅ Lire un capteur de température, pression et altitude (BMP280)

---

## Instructions

### Étape 1 : Connexion SSH (depuis Windows PowerShell)

Connectez-vous au Raspberry Pi via SSH depuis PowerShell :

```powershell
ssh jdupont@192.168.1.xxx
```

Remplacez `jdupont` par votre nom d'utilisateur créé dans Raspberry Pi Imager et `192.168.1.xxx` par l'adresse IP fournie en classe.

**Pour trouver l'adresse IP** :
```powershell
arp -a | findstr "b8-27-eb"
```

### Étape 2 : Créer votre espace de travail

```bash
mkdir -p ~/iot-lab
cd ~/iot-lab
```

### Étape 3 : Installer les dépendances

```bash
pip3 install --upgrade pip
pip3 install adafruit-circuitpython-bmp adafruit-blinka
```

### Étape 4 : Vérifier le capteur BMP280

```bash
sudo i2cdetect -y 1
```

Vous devriez voir `77` à l'adresse `0x77` (capteur BMP280).

⚠️ **IMPORTANT** : Le BMP280 fonctionne UNIQUEMENT en 3.3V ! Si VIN est connecté au 5V, le capteur ne répondra pas.

### Étape 5 : Créer le script de lecture

Créez le fichier `capteur.py` dans `~/iot-lab/` avec le contenu suivant :

```python
#!/usr/bin/env python3
"""
Lecture du capteur BMP280 - Température, Pression et Altitude
Formatif F1 - Semaine 1
"""

import board
import adafruit_bmp

# Création de l'objet capteur
i2c = board.I2C()
sensor = adafruit_bmp.BMP280_I2C(i2c)

# Lecture des valeurs
temperature = sensor.temperature
pression = sensor.pressure
altitude = sensor.altitude

# Affichage
print(f"Température : {temperature:.2f} °C")
print(f"Pression : {pression:.2f} hPa")
print(f"Altitude : {altitude:.1f} m")
```

### Étape 6 : Exécuter et valider

```bash
python3 capteur.py
```

Prenez une capture d'écran des résultats !

---

## Validation automatique

Pour recevoir une rétroaction automatique :

1. Poussez votre code sur GitHub (ce dépôt)
2. Les tests s'exécuteront automatiquement via GitHub Actions
3. Consultez l'onglet "Actions" pour voir les résultats
4. Corrigez selon la rétroaction fournie

### Tests automatisés

Les tests vérifient que :

| Test | Vérification | Points |
|------|-------------|--------|
| `test_requirements_present` | Fichier requirements.txt complet | 25% |
| `test_import_board` | Module board importable | 15% |
| `test_import_bmp280` | Module adafruit_bmp importable | 10% |
| `test_script_exists` | Script capteur.py présent | 15% |
| `test_script_has_required_imports` | Imports corrects | 15% |
| `test_script_creates_sensor` | Objet capteur BMP280 créé | 15% |
| `test_script_executes` | Script s'exécute sans erreur | 20% |
| `test_script_output_format` | Format de sortie correct (T°, P, Alt) | 20% |

---

## Livrables

Dans ce dépôt, vous devez avoir :

- [ ] `requirements.txt` — Liste des dépendances Python
- [ ] `capteur.py` — Votre script de lecture du capteur BMP280
- [ ] `captures/` — Dossier avec vos captures d'écran (optionnel pour l'auto-correction)

---

## Ressources

- [Guide de l'étudiant](../../deliverables/activites/semaine-1/labo/guide-étudiant.md)
- [Guide de dépannage](../../deliverables/activites/semaine-1/labo/guide-depannage.md)
- [Contenu d'apprentissage](../../deliverables/activites/semaine-1/theory/contenu-apprentissage.md)

---

## Rétroaction

Après avoir poussé votre code :

1. Allez dans l'onglet **Actions** de ce dépôt
2. Cliquez sur le workflow le plus récent
3. Lisez la rétroaction dans les logs de tests

**Note** : Ce formatif n'est pas noté. Son but est de vous donner une rétroaction rapide sur votre compréhension des concepts de base.

---

Bonne chance ! 🚀

# Formatif F1 — Introduction au Raspberry Pi et BMP280

**Cours** : 243-413-SH — Introduction aux objets connectés
**Semaine** : 1
**Type** : Formative (non notée)

---

## 📋 Description

Ce formatif vérifie que l'étudiant est capable de :
1. ✅ Se connecter au Raspberry Pi via SSH (depuis Windows)
2. ✅ Installer les bibliothèques Python nécessaires (BMP280)
3. ✅ Détecter un capteur I²C avec `i2cdetect`
4. ✅ Lire un capteur de température, pression et altitude (BMP280)

---

## 📁 Structure du dépôt

```
semaine-1-F1/
├── modele/                    # Modèle pour GitHub Classroom
│   ├── README.md             # Instructions pour les étudiants
│   ├── requirements.txt      # Dépendances Python
│   ├── capteur.py            # Script à compléter par l'étudiant
│   ├── correction.py         # Script de correction détaillée
│   ├── tests/                # Tests automatisés
│   │   ├── conftest.py       # Fixtures et configuration
│   │   └── test_formatif_f1.py # Tests pytest
│   └── .github/
│       └── workflows/
│           └── grade.yml     # Workflow GitHub Actions
├── devoir.yml                # Métadonnées du devoir
└── README.md                 # Ce fichier
```

---

## 🚀 Déploiement

### 1. Créer le dépôt modèle

```bash
cd modele/
git init
git add .
git commit -m "Initial commit - Formatif F1"
```

Créer le dépôt sur GitHub et pousser.

### 2. Créer le devoir dans GitHub Classroom

1. Aller sur [GitHub Classroom](https://classroom.github.com)
2. Nouveau devoir → Créer à partir d'un dépôt existant
3. Sélectionner le dépôt modèle créé
4. Configuration:
   - **Titre**: Formatif F1 — Introduction au Raspberry Pi et BMP280
   - **Type**: Formative
   - **Deadline**: Fin de la séance de laboratoire
   - **Invitation**: Lien ou liste d'étudiants

### 3. Publier aux étudiants

Partager le lien d'invitation avec les étudiants.

---

## 🧪 Tests automatisés

Les tests vérifient :

| Test | Vérification | Points | Indicateur |
|------|-------------|--------|------------|
| `test_requirements_present` | requirements.txt complet (BMP280) | 25% | IND-00SX-E |
| `test_import_board` | Module board importable | 15% | IND-00SX-E |
| `test_import_bmp280` | Module adafruit_bmp importable | 10% | IND-00SX-E |
| `test_script_exists` | Script capteur.py présent | 15% | IND-00SX-D |
| `test_script_has_required_imports` | Imports corrects | 15% | IND-00SX-D |
| `test_script_creates_sensor` | Objet capteur BMP280 créé | 15% | IND-00SX-D |
| `test_script_executes` | Script s'exécute sans erreur | 20% | IND-00SX-D |
| `test_script_output_format` | Format de sortie correct (T°, P, Alt) | 20% | IND-00SX-D |

---

## 📊 Correction

### Correction automatique

GitHub Actions exécute les tests automatiquement quand l'étudiant pousse son code.

### Correction manuelle (optionnelle)

```bash
python3 correction.py ../etudiants/du-pierre-julien-f1
```

Pour tous les étudiants d'un coup :

```bash
python3 correction.py --batch ../etudiants/ --export resultats_f1.xlsx
```

---

## 💡 Rétroaction

La rétroaction est générée automatiquement :

| Niveau | Message |
|--------|---------|
| **100%** | 🎉 Excellent! L'environnement est parfaitement configuré et le script est fonctionnel |
| **85%** | ✅ Très bon! Quelques améliorations mineures possibles |
| **60%** | 👍 Les bases sont en place. Peut être amélioré |
| **35%** | ⚠️ Partiellement correct. Vérifiez les points manquants |
| **0%** | ❌ Non fonctionnel. Consultez le guide de dépannage |

---

## 📚 Ressources associées

- [Guide de l'étudiant](../../deliverables/activites/semaine-1/labo/guide-étudiant.md)
- [Guide de dépannage](../../deliverables/activites/semaine-1/labo/guide-depannage.md)
- [Contenu d'apprentissage](../../deliverables/activites/semaine-1/theory/contenu-apprentissage.md)
- [Résultats attendus](../../deliverables/activites/semaine-1/labo/resultats-attendus.md)

---

## 📈 Indicateurs évalués

### IND-00SX-E — Exécution (Environnement & Déploiement)

**Critères de performance**: 2.1, 2.2, 2.3, 2.4, 2.6

**Niveaux de performance**:
- **0%** : L'environnement ne permet pas l'exécution
- **35%** : L'environnement fonctionne partiellement avec erreurs
- **60%** : L'environnement permet l'exécution fonctionnelle
- **85%** : L'environnement est complet et stable
- **100%** : L'environnement est optimisé et reproductible

### IND-00SX-D — Conception (Programmation)

**Critères de performance**: 4.1, 4.3

**Niveaux de performance**:
- **0%** : La logique applicative ne permet pas l'acquisition
- **35%** : La logique est partiellement fonctionnelle
- **60%** : La logique permet l'acquisition des données essentielles
- **85%** : La logique est entièrement fonctionnelle
- **100%** : La logique est fonctionnelle et optimisée

---

**Version** : 2.0
**Date de création** : 2026-01-16
**Dernière mise à jour** : 2026-01-19 (BMP280 + Windows)
**Auteur** : Agent pédagogique

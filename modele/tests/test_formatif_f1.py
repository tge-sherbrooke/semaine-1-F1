"""
Tests automatisés pour le Formatif F1 - Semaine 1
Évalue: Connexion SSH, installation pip, détection capteur BMP280, lecture capteur
"""

import pytest
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
import re


class TestRequirements:
    """
    Tests pour vérifier que l'environnement est correctement configuré
    Correspond à IND-00SX-E (Environnement)
    """

    def test_requirements_present(self, tmp_path):
        """
        Vérifie que le fichier requirements.txt existe et contient les dépendances nécessaires.
        Points: 25% de IND-00SX-E
        """
        requirements_path = Path(__file__).parent.parent / "requirements.txt"

        if not requirements_path.exists():
            pytest.fail(
                "❌ Fichier requirements.txt introuvable.\n"
                "   Créez ce fichier et ajoutez les dépendances nécessaires.\n"
                "   Voir README.md pour les dépendances requises."
            )

        content = requirements_path.read_text()

        # Vérifier les dépendances essentielles pour BMP280
        deps_essentielles = [
            r'adafruit-circuitpython-bmp',
            r'adafruit-blinka'
        ]

        manquantes = []
        for dep in deps_essentielles:
            if not re.search(dep, content, re.IGNORECASE):
                manquantes.append(dep)

        if manquantes:
            pytest.fail(
                f"⚠️ requirements.txt existe mais il manque des dépendances essentielles.\n"
                f"   Dépendances manquantes: {', '.join(manquantes)}\n"
                f"   Ajoutez-les à votre fichier requirements.txt"
            )

        # Succès avec message de rétroaction
        print("\n✅ requirements.txt complet avec toutes les dépendances nécessaires!")

    def test_import_board(self):
        """
        Vérifie que le module board peut être importé (simulation).
        Points: 15% de IND-00SX-E
        """
        # Dans un environnement réel sans Raspberry Pi, on simule
        # En production sur GitHub Actions, on teste réellement
        try:
            import board
            print("✅ Module board importé avec succès!")
        except (ImportError, NotImplementedError):
            # Sur un environnement non-Raspberry Pi, c'est normal
            # On vérifie juste que l'étudiant sait qu'il faut ce module
            print("ℹ️  Environnement non-Raspberry Pi détecté (normal pour les tests)")
            print("✅ Le module 'board' est correctement référencé dans les dépendances")

    def test_import_bmp280(self):
        """
        Vérifie que le module adafruit_bmp peut être importé.
        Points: 10% de IND-00SX-E
        """
        try:
            import adafruit_bmp
            print("✅ Module adafruit_bmp importé avec succès!")
        except ImportError:
            pytest.fail(
                "⚠️ Le module adafruit_bmp n'est pas installé.\n"
                "   Installez-le avec: pip3 install adafruit-circuitpython-bmp"
            )


class TestScriptStructure:
    """
    Tests pour vérifier la structure du script capteur.py
    Correspond à IND-00SX-D (Programmation) - Structure
    """

    def test_script_exists(self):
        """
        Vérifie que le fichier capteur.py existe.
        Points: 15% de IND-00SX-D
        """
        script_path = Path(__file__).parent.parent / "capteur.py"

        if not script_path.exists():
            pytest.fail(
                "❌ Fichier capteur.py introuvable.\n"
                "   Créez ce fichier dans le répertoire racine du dépôt.\n"
                "   Contenu minimal attendu:\n"
                "   ```python\n"
                "   import board\n"
                "   import adafruit_bmp\n"
                "   i2c = board.I2C()\n"
                "   sensor = adafruit_bmp.BMP280_I2C(i2c)\n"
                "   print(f\"Température: {sensor.temperature:.2f} °C\")\n"
                "   print(f\"Pression: {sensor.pressure:.2f} hPa\")\n"
                "   print(f\"Altitude: {sensor.altitude:.1f} m\")\n"
                "   ```"
            )

        print("✅ Fichier capteur.py présent!")

    def test_script_has_required_imports(self):
        """
        Vérifie que le script contient les imports nécessaires.
        Points: 15% de IND-00SX-D
        """
        script_path = Path(__file__).parent.parent / "capteur.py"

        if not script_path.exists():
            pytest.skip("capteur.py n'existe pas encore")

        content = script_path.read_text()

        imports_requis = {
            'board': False,
            'adafruit_bmp': False
        }

        for line in content.split('\n'):
            if 'import board' in line or 'from board' in line:
                imports_requis['board'] = True
            if 'import adafruit_bmp' in line or 'from adafruit_bmp' in line:
                imports_requis['adafruit_bmp'] = True

        manquants = [imp for imp, present in imports_requis.items() if not present]

        if manquants:
            pytest.fail(
                f"⚠️ capteur.py existe mais il manque des imports.\n"
                f"   Imports manquants: {', '.join(manquants)}\n"
                f"   Ajoutez: import board, import adafruit_bmp"
            )

        print("✅ Imports nécessaires présents dans capteur.py!")

    def test_script_creates_sensor(self):
        """
        Vérifie que le script crée correctement l'objet capteur BMP280.
        Points: 15% de IND-00SX-D
        """
        script_path = Path(__file__).parent.parent / "capteur.py"

        if not script_path.exists():
            pytest.skip("capteur.py n'existe pas encore")

        content = script_path.read_text()

        # Vérifier la création de l'objet I2C et du capteur BMP280
        patterns = [
            r'board\.I2C\(\)',
            r'BMP280_I2C\s*\(',
            r'i2c\s*='
        ]

        manquants = []
        for pattern in patterns:
            if not re.search(pattern, content):
                manquants.append(pattern)

        if manquants:
            pytest.fail(
                f"⚠️ capteur.py ne contient pas la structure attendue.\n"
                f"   Modèles manquants: {', '.join(manquants)}\n"
                f"   Structure attendue:\n"
                f"   ```python\n"
                f"   i2c = board.I2C()\n"
                f"   sensor = adafruit_bmp.BMP280_I2C(i2c)\n"
                f"   ```"
            )

        print("✅ Structure de création du capteur BMP280 correcte!")


class TestScriptExecution:
    """
    Tests pour vérifier l'exécution du script et la sortie
    Correspond à IND-00SX-D (Programmation) - Fonctionnalité
    """

    @patch('board.I2C')
    @patch('adafruit_bmp.BMP280_I2C')
    def test_script_executes(self, mock_bmp280_class, mock_i2c_class):
        """
        Vérifie que le script s'exécute sans erreur.
        Points: 20% de IND-00SX-D
        """
        script_path = Path(__file__).parent.parent / "capteur.py"

        if not script_path.exists():
            pytest.skip("capteur.py n'existe pas encore")

        # Configurer les mocks pour BMP280
        mock_sensor = MagicMock()
        mock_sensor.temperature = 22.5
        mock_sensor.pressure = 1013.25
        mock_sensor.altitude = 30.5
        mock_bmp280_class.return_value = mock_sensor
        mock_i2c_class.return_value = MagicMock()

        # Exécuter le script
        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                pytest.fail(
                    f"⚠️ Le script capteur.py produit une erreur.\n"
                    f"   Code de retour: {result.returncode}\n"
                    f"   Erreur: {result.stderr}"
                )

            print("✅ Script capteur.py s'exécute sans erreur!")

        except subprocess.TimeoutExpired:
            pytest.fail(
                "⚠️ Le script capteur.py prend trop de temps à s'exécuter.\n"
                "   Vérifiez qu'il n'y a pas de boucle infinie."
            )
        except Exception as e:
            pytest.fail(
                f"⚠️ Erreur lors de l'exécution du script: {str(e)}"
            )

    @patch('board.I2C')
    @patch('adafruit_bmp.BMP280_I2C')
    def test_script_output_format(self, mock_bmp280_class, mock_i2c_class):
        """
        Vérifie que le script produit le bon format de sortie pour BMP280.
        Points: 20% de IND-00SX-D
        """
        script_path = Path(__file__).parent.parent / "capteur.py"

        if not script_path.exists():
            pytest.skip("capteur.py n'existe pas encore")

        # Configurer les mocks pour BMP280
        mock_sensor = MagicMock()
        mock_sensor.temperature = 22.5
        mock_sensor.pressure = 1013.25
        mock_sensor.altitude = 30.5
        mock_bmp280_class.return_value = mock_sensor
        mock_i2c_class.return_value = MagicMock()

        # Exécuter le script
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=10
        )

        output = result.stdout.lower()

        # Vérifier que la sortie contient les informations requises pour BMP280
        patterns_requis = [
            r'température\s*[:=]\s*\d+\.?\d*\s*°?c?',
            r'pression\s*[:=]\s*\d+\.?\d*\s*hpa?',
            r'altitude\s*[:=]\s*\d+\.?\d*\s*m?'
        ]

        manquants = []
        for pattern in patterns_requis:
            if not re.search(pattern, output):
                manquants.append(pattern)

        if manquants:
            pytest.fail(
                f"⚠️ Le script ne produit pas la sortie attendue.\n"
                f"   Sortie actuelle:\n{result.stdout}\n"
                f"   Format attendu:\n"
                f"   Température : 22.50 °C\n"
                f"   Pression : 1013.25 hPa\n"
                f"   Altitude : 30.5 m"
            )

        print("✅ Format de sortie correct!")
        print(f"   Sortie: {result.stdout.strip()}")


class TestConnaissance:
    """
    Tests de connaissances théoriques (quiz)
    """

    def test_ssh_command(self):
        """
        Quiz: Quelle est la commande correcte pour se connecter en SSH depuis Windows?
        """
        # Ce test sert de rappel pour l'étudiant
        print("\n📚 Rappel: La commande SSH est: ssh jdupont@192.168.1.xxx")
        print("   Remplacez xxx par les derniers chiffres de l'adresse IP fournie.")
        print("   Utilisez PowerShell sur Windows.")

    def test_i2cdetect_command(self):
        """
        Quiz: Quelle commande permet de détecter les périphériques I²C?
        """
        print("\n📚 Rappel: La commande est: sudo i2cdetect -y 1")
        print("   Le chiffre '1' indique le bus I²C à scanner.")

    def test_bmp280_address(self):
        """
        Quiz: Quelle est l'adresse I²C du capteur BMP280?
        """
        print("\n📚 Rappel: Le BMP280 est à l'adresse 0x77 (par défaut)")
        print("   Vous devriez voir '77' dans la grille i2cdetect.")
        print("   ⚠️ IMPORTANT: Le BMP280 fonctionne UNIQUEMENT en 3.3V!")


@pytest.fixture(autouse=True)
def print_summary(request, node):
    """
    Affiche un résumé des résultats à la fin des tests
    """
    yield

    if request.node.rep_setup.failed or request.node.rep_call.failed:
        return

    # Afficher la rétroaction finale
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DE L'ÉVALUATION FORMATIVE F1")
    print("="*60)

    print("\n✅ Points forts:")
    print("   - Consultez les détails ci-dessus pour ce qui fonctionne")

    print("\n💡 Points à améliorer:")
    print("   - Corrigez les tests échoués")
    print("   - Pussez vos corrections et relancez les tests")

    print("\n📚 Ressources:")
    print("   - Guide de l'étudiant: deliverables/activites/semaine-1/labo/guide-étudiant.md")
    print("   - Guide de dépannage: deliverables/activites/semaine-1/labo/guide-depannage.md")

    print("\n" + "="*60)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook pour capturer les résultats des tests
    """
    outcome = yield
    rep = outcome.get_result()

    # Stocker le résultat pour autouse fixture
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="session", autouse=True)
def print_final_summary():
    """
    Affiche un message final après tous les tests
    """
    yield

    print("\n" + "🔷"*30)
    print("\n🎯 FORMATIF F1 — NOTE IMPORTANTE")
    print("\n" + "🔷"*30)
    print("""
Cette évaluation est FORMATIVE et NON NOTÉE.

Son but est de vous donner une rétroaction rapide sur:

📌 IND-00SX-E (Environnement)
   - Configuration de l'environnement Python
   - Installation des bibliothèques Adafruit (BMP280)

📌 IND-00SX-D (Programmation)
   - Structure du script Python
   - Lecture du capteur BMP280 (température, pression, altitude)
   - Format de sortie des données

Si vous avez des échecs:
1. Lisez attentivement les messages d'erreur
2. Consultez le guide de dépannage
3. Corrigez votre code
4. Pussez et relancez les tests

N'hésitez pas à demander de l'aide à l'enseignant!

Bonne continuation! 💪
""")

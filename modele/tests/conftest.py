"""
Fixtures et mocks pour les tests du formatif F1
Simule le matériel Raspberry Pi et les capteurs
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour importer capteur.py
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def mock_board():
    """
    Simule le module board pour GPIO/I2C
    """
    with patch('board.I2C') as mock_i2c:
        # Créer un mock pour le bus I2C
        i2c_bus = MagicMock()
        mock_i2c.return_value = i2c_bus
        yield i2c_bus


@pytest.fixture
def mock_bmp280():
    """
    Simule le capteur BMP280 avec des valeurs réalistes
    """
    sensor = MagicMock()
    sensor.temperature = 22.5  # Valeur réaliste en °C
    sensor.pressure = 1013.25  # Valeur réaliste en hPa
    sensor.altitude = 30.5  # Valeur réaliste en mètres

    # Simuler la classe avec le constructeur
    SensorClass = MagicMock(return_value=sensor)
    SensorClass.temperature = 22.5
    SensorClass.pressure = 1013.25
    SensorClass.altitude = 30.5

    return SensorClass


@pytest.fixture
def mock_i2c_detect_output():
    """
    Sortie typique de i2cdetect pour un capteur BMP280 à 0x77
    """
    return """     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 77 --
"""


@pytest.fixture
def sample_output():
    """
    Sortie attendue du script capteur.py pour BMP280
    """
    return """Température : 22.50 °C
Pression : 1013.25 hPa
Altitude : 30.5 m"""


# Indicateurs évalués et leurs pondérations
INDICATEURS = {
    "IND-00SX-E": {
        "ponderation": 100,
        "critere": "Exécution — Environnement & Déploiement",
        "description": "Préparer l'environnement et déployer l'application"
    },
    "IND-00SX-D": {
        "ponderation": 100,
        "critere": "Conception — Programmation",
        "description": "Programmer la logique applicative"
    }
}


def calculer_note_et_retroaction(resultats_tests):
    """
    Calcule la note et génère la rétroaction selon les grilles permanentes.

    Args:
        resultats_tests: Dict avec les résultats des tests

    Returns:
        tuple: (note_finale, feedback_dict)
    """
    note_finale = 0
    feedback = {
        "IND-00SX-E": {
            "niveau": 0,
            "message": ""
        },
        "IND-00SX-D": {
            "niveau": 0,
            "message": ""
        }
    }

    # Évaluer IND-00SX-E (Environnement)
    # Tests: requirements.txt, imports fonctionnels
    score_e = 0
    if resultats_tests.get("test_requirements_present", False):
        score_e += 50
    if resultats_tests.get("test_imports", False):
        score_e += 50

    niveau_e = _determiner_niveau(score_e, "IND-00SX-E")
    feedback["IND-00SX-E"]["niveau"] = niveau_e
    feedback["IND-00SX-E"]["message"] = _generer_message_feedback("IND-00SX-E", niveau_e, score_e)

    # Évaluer IND-00SX-D (Programmation)
    # Tests: script existe, structure correcte, sortie correcte
    score_d = 0
    if resultats_tests.get("test_script_exists", False):
        score_d += 30
    if resultats_tests.get("test_script_structure", False):
        score_d += 30
    if resultats_tests.get("test_script_output", False):
        score_d += 40

    niveau_d = _determiner_niveau(score_d, "IND-00SX-D")
    feedback["IND-00SX-D"]["niveau"] = niveau_d
    feedback["IND-00SX-D"]["message"] = _generer_message_feedback("IND-00SX-D", niveau_d, score_d)

    # Note finale (moyenne pondérée)
    note_finale = (score_e * 0.5) + (score_d * 0.5)

    return note_finale, feedback


def _determiner_niveau(score, indicateur):
    """
    Détermine le niveau selon les grilles permanentes (0%, 35%, 60%, 85%, 100%).
    """
    if score >= 100:
        return 100
    elif score >= 85:
        return 85
    elif score >= 60:
        return 60
    elif score >= 35:
        return 35
    else:
        return 0


def _generer_message_feedback(indicateur, niveau, score):
    """
    Génère un message de rétroaction personnalisé selon le niveau.
    """
    messages = {
        "IND-00SX-E": {
            100: "🎉 Excellent ! L'environnement est parfaitement configuré. "
                 "Les dépendances sont correctement installées et les imports fonctionnent.",
            85: "✅ Très bon ! L'environnement est bien configuré. "
                "Tout fonctionne correctement.",
            60: "👍 L'environnement de base est en place. "
                "Quelques améliorations mineures possibles.",
            35: "⚠️ L'environnement est partiellement configuré. "
                "Vérifiez que toutes les dépendances sont listées dans requirements.txt.",
            0: "❌ L'environnement n'est pas configuré. "
               "Assurez-vous d'avoir un requirements.txt complet et que les imports fonctionnent."
        },
        "IND-00SX-D": {
            100: "🎉 Parfait ! Le script est fonctionnel, bien structuré et produit le résultat attendu.",
            85: "✅ Très bon travail ! Le script fonctionne correctement et affiche les données.",
            60: "👍 Le script fonctionne et affiche les données essentielles. "
                "Peut être amélioré pour le format.",
            35: "⚠️ Le script existe mais a des problèmes de structure ou de sortie. "
                "Vérifiez le format d'affichage demandé.",
            0: "❌ Le script n'est pas fonctionnel ou absent. "
               "Créez un script capteur.py qui lit et affiche la température, pression et altitude."
        }
    }

    return messages.get(indicateur, {}).get(niveau, "Rétroaction non disponible")


@pytest.fixture
def indicateur_eval():
    """
    Fixture pour accéder aux indicateurs dans les tests
    """
    return INDICATEURS

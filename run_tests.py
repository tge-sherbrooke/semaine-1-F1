# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Test runner local pour le Formatif F1 - Semaine 1

Ce script execute les tests localement sur le Raspberry Pi et cree
des fichiers marqueurs qui seront verifies par GitHub Actions.

Usage: python3 run_tests.py
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Couleurs ANSI pour le terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")


def print_success(text):
    print(f"{Colors.GREEN}+ {text}{Colors.END}")


def print_error(text):
    print(f"{Colors.RED}x {text}{Colors.END}")


def print_warning(text):
    print(f"{Colors.YELLOW}! {text}{Colors.END}")


def check_ssh_key():
    """
    Verifie qu'une cle SSH existe sur le Pi et teste la connexion GitHub.
    """
    print_header("VERIFICATION SSH ET GITHUB")

    ssh_dir = Path.home() / ".ssh"
    # Chercher d'abord la cle specifique au cours IoT
    pub_keys = [
        ssh_dir / "id_ed25519_iot.pub",  # Cle recommandee pour le cours
        ssh_dir / "id_ed25519.pub",
        ssh_dir / "id_rsa.pub",
    ]

    key_found = False
    key_path = None

    for key_path in pub_keys:
        if key_path.exists():
            key_found = True
            print_success(f"Cle SSH publique trouvee: {key_path.name}")

            # Lire le contenu de la cle publique
            key_content = key_path.read_text().strip()
            print(f"   {key_content[:40]}...")
            break

    if not key_found:
        print_error("Aucune cle SSH publique trouvee")
        print("\nPour generer une cle SSH sur le Raspberry Pi:")
        print("   ssh-keygen -t ed25519 -C \"iot-cegep@etu.cegep.qc.ca\" -f ~/.ssh/id_ed25519_iot")
        print("   (Appuyez 3x sur Entree pour les valeurs par defaut)")
        print("\nPour afficher la cle publique:")
        print("   cat ~/.ssh/id_ed25519_iot.pub")
        print("\nPour ajouter la cle a GitHub:")
        print("   1. Allez sur https://github.com -> Settings -> SSH and GPG keys")
        print("   2. Cliquez sur 'New SSH key'")
        print("   3. Collez la cle publique")
        return False

    # Verifier la configuration SSH pour GitHub
    config_file = ssh_dir / "config"
    if config_file.exists():
        config_content = config_file.read_text()
        if "github.com" in config_content and "id_ed25519_iot" in config_content:
            print_success("Fichier ~/.ssh/config configure pour GitHub")
        else:
            print_warning("Fichier ~/.ssh/config existe mais n'est pas configure pour GitHub")
            print("\nPour configurer SSH pour GitHub:")
            print('   cat > ~/.ssh/config << \'EOF\'')
            print('   Host github.com')
            print('       HostName github.com')
            print('       User git')
            print('       IdentityFile ~/.ssh/id_ed25519_iot')
            print('       IdentitiesOnly yes')
            print('   EOF')
            print('   chmod 600 ~/.ssh/config')
    else:
        print_warning("Fichier ~/.ssh/config introuvable")

    # Tester la connexion GitHub
    print("\nTest de connexion avec GitHub...")
    try:
        result = subprocess.run(
            ['ssh', '-T', 'git@github.com'],
            capture_output=True, text=True, timeout=10
        )
        # GitHub retourne un code non-zero mais avec le message "successfully authenticated"
        if 'successfully authenticated' in result.stderr or result.returncode == 1:
            print_success("Connexion GitHub fonctionnelle!")
            # Extraire le nom d'utilisateur si possible
            if 'Hi ' in result.stderr:
                username = result.stderr.split('Hi ')[1].split('!')[0]
                print(f"   Authentifie en tant que: {username}")
        else:
            print_warning("Connexion GitHub uncertaine")
            print(f"   stderr: {result.stderr[:100]}")
    except subprocess.TimeoutExpired:
        print_warning("Timeout lors de la connexion GitHub - verifiez votre connexion internet")
    except FileNotFoundError:
        print_warning("SSH non trouve - installez: sudo apt install openssh-client")
    except Exception as e:
        print_warning(f"Erreur de connexion GitHub: {e}")
        print("\nPour tester manuellement:")
        print("   ssh -T git@github.com")

    # Creer le marqueur SSH
    marker = Path(__file__).parent / ".test_markers" / "ssh_key_verified.txt"
    marker.parent.mkdir(exist_ok=True)
    marker.write_text(f"SSH key verified: {datetime.now().isoformat()}\n")
    marker.write_text(f"Key file: {key_path.name}\n")
    print_success(f"Marqueur SSH cree: {marker}")

    return True


def check_aht20_script():
    """
    Verifie le script test_aht20.py.
    """
    print_header("VERIFICATION TEST_AHT20.PY")

    script_path = Path(__file__).parent / "test_aht20.py"

    if not script_path.exists():
        print_error("Fichier test_aht20.py introuvable")
        return False

    print_success("Fichier test_aht20.py trouve")

    # Verifier la syntaxe
    try:
        with open(script_path) as f:
            compile(f.read(), script_path, 'exec')
        print_success("Syntaxe Python valide")
    except SyntaxError as e:
        print_error(f"Erreur de syntaxe ligne {e.lineno}: {e.msg}")
        return False

    # Verifier les imports
    content = script_path.read_text()
    required = ['board', 'adafruit_ahtx0']

    for imp in required:
        if imp in content:
            print_success(f"Import trouve: {imp}")
        else:
            print_error(f"Import manquant: {imp}")
            return False

    # Verifier les dependances UV
    if 'dependencies' in content and 'adafruit-circuitpython-ahtx0' in content:
        print_success("Dependances UV configurees")
    else:
        print_warning("Dependances UV non trouvees (decommentees dans le script?)")

    # Creer le marqueur
    marker = Path(__file__).parent / ".test_markers" / "aht20_script_verified.txt"
    marker.write_text(f"AHT20 script verified: {datetime.now().isoformat()}\n")
    print_success(f"Marqueur AHT20 cree: {marker}")

    return True


def check_neoslider_script():
    """
    Verifie le script test_neoslider.py.
    """
    print_header("VERIFICATION TEST_NEOSLIDER.PY")

    script_path = Path(__file__).parent / "test_neoslider.py"

    if not script_path.exists():
        print_warning("test_neoslider.py introuvable (optionnel)")
        return True  # Non obligatoire

    print_success("Fichier test_neoslider.py trouve")

    # Verifier la syntaxe
    try:
        with open(script_path) as f:
            compile(f.read(), script_path, 'exec')
        print_success("Syntaxe Python valide")
    except SyntaxError as e:
        print_error(f"Erreur de syntaxe ligne {e.lineno}: {e.msg}")
        return False

    # Verifier les imports
    content = script_path.read_text()
    required = ['board', 'adafruit_seesaw']

    for imp in required:
        if imp in content:
            print_success(f"Import trouve: {imp}")
        else:
            print_error(f"Import manquant: {imp}")
            return False

    # Creer le marqueur
    marker = Path(__file__).parent / ".test_markers" / "neoslider_script_verified.txt"
    marker.write_text(f"NeoSlider script verified: {datetime.now().isoformat()}\n")
    print_success(f"Marqueur NeoSlider cree: {marker}")

    return True


def run_hardware_tests():
    """
    Tente d'executer les tests materiels (si sur Raspberry Pi).
    """
    print_header("TESTS MATERIEL (Raspberry Pi)")

    # Verifier si on est sur un Raspberry Pi
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
            is_rpi = 'Raspberry Pi' in cpuinfo or 'Broadcom' in cpuinfo
    except:
        is_rpi = False

    if not is_rpi:
        print_warning("Pas sur Raspberry Pi - tests materiels skipes")
        print("   Executez ce script sur le Raspberry Pi pour les tests materiels")
        return True

    print_success("Raspberry Pi detecte")

    # Verifier i2cdetect
    try:
        result = subprocess.run(
            ['sudo', 'i2cdetect', '-y', '1'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            output = result.stdout
            if '38' in output:
                print_success("AHT20 detecte a l'adresse 0x38")
            else:
                print_warning("AHT20 non detecte a 0x38 - verifiez le cablage STEMMA QT")

            if '30' in output:
                print_success("NeoSlider detecte a l'adresse 0x30")
            else:
                print_warning("NeoSlider non detecte a 0x30 (optionnel)")

            # Creer le marqueur materiel
            marker = Path(__file__).parent / ".test_markers" / "hardware_detected.txt"
            marker.write_text(f"Hardware scan: {datetime.now().isoformat()}\n{output}\n")
            print_success(f"Marqueur materiel cree: {marker}")
        else:
            print_error("i2cdetect a echoue")
            return False
    except FileNotFoundError:
        print_warning("i2cdetect non trouve - installez: sudo apt install i2c-tools")
    except subprocess.TimeoutExpired:
        print_warning("i2cdetect timeout - verifiez I2C")
    except Exception as e:
        print_warning(f"Erreur i2cdetect: {e}")

    return True


def update_gitignore():
    """
    Met a jour .gitignore pour permettre de commettre les marqueurs de tests.
    Supprime la ligne '.test_markers/' du .gitignore pour permettre aux etudiants
    de pousser les marqueurs crees par run_tests.py.
    """
    gitignore_path = Path(__file__).parent / ".gitignore"
    marker_dir = Path(__file__).parent / ".test_markers"

    # Si les marqueurs existent, on permet de les commettre
    if not marker_dir.exists():
        return

    if not gitignore_path.exists():
        return

    # Lire le .gitignore actuel
    lines = gitignore_path.read_text().splitlines()

    # Filtrer les lignes qui excluent .test_markers
    new_lines = []
    modified = False
    for line in lines:
        # Ignorer les patterns qui excluent .test_markers ou son contenu
        if '.test_markers' in line and not line.strip().startswith('#'):
            # Remplacer par un commentaire explicatif
            if not modified:
                new_lines.append('# .test_markers/ is now allowed (created by run_tests.py)')
                modified = True
        else:
            new_lines.append(line)

    if modified:
        gitignore_path.write_text('\n'.join(new_lines) + '\n')
        print_success(".gitignore mis a jour - les marqueurs peuvent etre commites")


def create_test_summary():
    """
    Cree un resume des tests pour GitHub Actions.
    """
    marker_dir = Path(__file__).parent / ".test_markers"
    summary_file = marker_dir / "test_summary.txt"

    markers = list(marker_dir.glob("*_verified.txt")) + list(marker_dir.glob("*_detected.txt"))

    summary = f"""Test Summary for Formatif F1
Generated: {datetime.now().isoformat()}
Tests Run: {len(markers)}

Markers:
"""
    for marker in sorted(markers):
        summary += f"  - {marker.stem}: {marker.read_text().strip()}\n"

    summary_file.write_text(summary)
    print_success(f"Resume des tests cree: {summary_file}")


def main():
    """
    Fonction principale.
    """
    print(f"\n{Colors.BOLD}Formatif F1 - Test Runner Local{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")

    results = {
        "SSH": check_ssh_key(),
        "AHT20": check_aht20_script(),
        "NeoSlider": check_neoslider_script(),
        "Hardware": run_hardware_tests(),
    }

    # Creer le resume
    create_test_summary()

    # Afficher le resultat final
    print_header("RESULTAT FINAL")

    all_passed = all(results.values())

    for test, passed in results.items():
        if passed:
            print_success(f"{test}: OK")
        else:
            print_error(f"{test}: ECHEC")

    print()

    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}TOUS LES TESTS SONT PASSES!{Colors.END}")

        # Met a jour .gitignore pour permettre de commettre les marqueurs
        update_gitignore()

        print("\nVous pouvez maintenant pousser vos modifications:")
        print("   git add .")
        print("   git commit -m \"feat: tests locaux passes\"")
        print("   git push")

        # Creer le marqueur final de succes
        marker = Path(__file__).parent / ".test_markers" / "all_tests_passed.txt"
        marker.write_text(f"All tests passed: {datetime.now().isoformat()}\n")

        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}CERTAINS TESTS ONT ECHOUE{Colors.END}")
        print("\nCorrigez les erreurs ci-dessus et relancez:")
        print("   python3 run_tests.py")

        return 1


if __name__ == "__main__":
    sys.exit(main())

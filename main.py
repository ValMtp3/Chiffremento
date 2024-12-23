import argparse
import os

from file_crypto import encrypt_file, decrypt_file
from key_manager import key


def validate_file(file_path):
    """Vérifie si le fichier existe."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Erreur : Le fichier '{file_path}' n'existe pas.")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chiffrement et déchiffrement de fichiers")
    parser.add_argument("file", help="Chemin du fichier à chiffrer ou à déchiffrer")
    parser.add_argument("action", choices=["encrypt", "decrypt"],
                        help="Action à effectuer : 'encrypt' pour chiffrer, 'decrypt' pour déchiffrer")
    args = parser.parse_args()

    file_path = args.file
    action = args.action

    try:
        # Valider que le fichier existe
        validate_file(file_path)

        # Exécuter l'action spécifiée
        if action == "encrypt":
            encrypt_file(file_path, key)
            print(f"Le fichier {file_path} a été chiffré.")
        elif action == "decrypt":
            decrypt_file(file_path, key)
            print(f"Le fichier {file_path} a été déchiffré.")
    except FileNotFoundError as e:
        print(f"Erreur : {e}")
    except Exception as e:
        print(f"Une erreur inattendue s'est produite : {e}")

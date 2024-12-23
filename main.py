import argparse
import os

from file_crypto import encrypt_file, decrypt_file, overwrite_file
from key_manager import key


def validate_file(file_path):
    """Vérifie si le fichier existe."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Erreur : Le fichier '{file_path}' n'existe pas.")
    return True


if __name__ == "__main__":
    # Création d'un parseur d'arguments pour la ligne de commande
    parser = argparse.ArgumentParser(description="Chiffrement et déchiffrement de fichiers")

    # Ajout des arguments attendus
    parser.add_argument("file", help="Chemin du fichier à chiffrer ou à déchiffrer")
    parser.add_argument("action", choices=["encrypt", "decrypt"],
                        help="Action à effectuer : 'encrypt' pour chiffrer, 'decrypt' pour déchiffrer")
    parser.add_argument("--delete", action="store_true", help="Supprime le fichier original après l'opération")

    # Analyse des arguments passés en ligne de commande
    args = parser.parse_args()

    # Récupération des valeurs des arguments
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

        # Supprimer le fichier original si l'option --del est spécifiée
        if args.delete:
            overwrite_file(file_path)
            os.remove(file_path)
            print(f"Le fichier original {file_path} a été supprimé.")

    except FileNotFoundError as e:
        # Gérer l'erreur si le fichier n'existe pas
        print(f"Erreur : {e}")
    except Exception as e:
        # Gérer toute autre erreur inattendue
        print(f"Une erreur inattendue s'est produite : {e}")

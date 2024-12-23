import os

from file_crypto import encrypt_file, decrypt_file
from key_manager import generate_key, load_key


# Fonction pour demander le nom du fichier
def get_file_name():
    return input("Entrez le nom du fichier : ")


# Fonction pour demander l'action à effectuer
def get_action():
    return input("Voulez-vous chiffrer ou déchiffrer le fichier ? (c/d) : ")


# Exemple d'utilisation
if not os.path.exists("secret.key"):
    generate_key()

key = load_key()
file_path = get_file_name()
action = get_action()

if action == 'c':
    encrypt_file(file_path, key)
    print(f"Le fichier {file_path} a été chiffré.")
elif action == 'd':
    decrypt_file(file_path, key)
    print(f"Le fichier {file_path} a été déchiffré.")
else:
    print("Action non reconnue.")

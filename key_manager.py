import os

from cryptography.fernet import Fernet


# Générer une clé de chiffrement et la sauvegarder dans un fichier
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as filekey:
        filekey.write(key)


# Charger la clé de chiffrement depuis un fichier
def load_key():
    return open("secret.key", "rb").read()


# Générer la clé si elle n'existe pas
if not os.path.exists("secret.key"):
    generate_key()

key = load_key()

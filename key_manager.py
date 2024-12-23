from cryptography.fernet import Fernet


# Générer une clé de chiffrement et la sauvegarder dans un fichier
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as filekey:
        filekey.write(key)


# Charger la clé de chiffrement depuis un fichier
def load_key():
    return open("secret.key", "rb").read()

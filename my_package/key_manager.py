from cryptography.fernet import Fernet

from my_package.db import save_key, get_key

key_name = "default_key"


# Générer une clé de chiffrement et l'enregistrer dans MongoDB
def generate_key():
    key = Fernet.generate_key()
    public_key = "fake_public_key"

    # Sauvegarde de la clé privée (chiffrée) et publique dans MongoDB
    save_key(key_name, key.decode(), public_key)
    return key


# Charger la clé de chiffrement depuis MongoDB
def load_key():
    try:
        key_data = get_key(key_name)
        return key_data["cle_privee_chiffree"].encode()  # Retourne la clé en bytes
    except ValueError as e:
        print(e)
        raise
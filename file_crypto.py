import os

from cryptography.fernet import Fernet, InvalidToken


# Fonction pour chiffrer un fichier
def encrypt_file(file_path, key):
    cipher_suite = Fernet(key)
    if not os.path.exists(file_path):
        print(f"Erreur : Le fichier {file_path} n'existe pas.")
        return
    with open(file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = cipher_suite.encrypt(file_data)
    with open(file_path + '.encrypted', 'wb') as file:
        file.write(encrypted_data)


# Fonction pour déchiffrer un fichier
def decrypt_file(file_path, key):
    cipher_suite = Fernet(key)
    if not os.path.exists(file_path):
        print(f"Erreur : Le fichier {file_path} n'existe pas.")
        return
    if not file_path.endswith('.encrypted'):
        print(f"Erreur : Le fichier {file_path} n'est pas un fichier chiffré.")
        return
    try:
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = cipher_suite.decrypt(encrypted_data)  # Peut lever InvalidToken
    except InvalidToken:
        print(f"Erreur : Échec du déchiffrement. La clé est invalide ou les données sont corrompues.")
        return  # Retourne None pour signaler l'échec
    original_file_path = file_path.replace('.encrypted', '')
    with open(original_file_path, 'wb') as file:
        file.write(decrypted_data)


# Fonction pour écraser un fichier après une opération
def overwrite_file(file_path):
    """Écrase le contenu d'un fichier en remplaçant par des zéros."""
    if not os.path.exists(file_path):
        print(f"Erreur : Le fichier {file_path} n'existe pas pour être écrasé.")
        return

    try:
        file_size = os.path.getsize(file_path)  # Taille du fichier
        with open(file_path, 'wb') as file:
            file.write(b'\x00' * file_size)  # Écrase le contenu avec des zéros
    except Exception as e:
        print(f"Erreur lors de l'écrasement du fichier {file_path} : {e}")

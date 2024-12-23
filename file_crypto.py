import os

from cryptography.fernet import Fernet


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
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    original_file_path = file_path.replace('.encrypted', '')
    with open(original_file_path, 'wb') as file:
        file.write(decrypted_data)

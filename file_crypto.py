import os
import shutil
import zipfile

from cryptography.fernet import Fernet, InvalidToken


# Fonction pour chiffrer un fichier
def encrypt_file(file_path, key, display_callback=None):
    cipher_suite = Fernet(key)
    if not os.path.exists(file_path):
        if display_callback:
            display_callback(f"Erreur : Le fichier {file_path} n'existe pas.")
        return
    with open(file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = cipher_suite.encrypt(file_data)
    with open(file_path + '.enc', 'wb') as file:
        file.write(encrypted_data)

    # Appeler un éventuel callback pour afficher le nom simplifié
    if display_callback:
        display_callback(os.path.basename(file_path) + ".enc")


# Fonction pour déchiffrer un fichier
def decrypt_file(file_path, key):
    cipher_suite = Fernet(key)
    if not os.path.exists(file_path):
        print(f"Erreur : Le fichier {file_path} n'existe pas.")
        return
    if not file_path.endswith('.enc'):
        print(f"Erreur : Le fichier {file_path} n'est pas un fichier chiffré.")
        return
    try:
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = cipher_suite.decrypt(encrypted_data)  # Peut lever InvalidToken
    except InvalidToken:
        print(f"Erreur : Échec du déchiffrement. La clé est invalide ou les données sont corrompues.")
        return  # Retourne None pour signaler l'échec
    original_file_path = file_path.replace('.enc', '')
    with open(original_file_path, 'wb') as file:
        file.write(decrypted_data)


# Fonction pour écraser un fichier après une opération
def overwrite_file(file_path, display_callback=None):
    """Écrase le contenu d'un fichier en remplaçant par des zéros."""
    if not os.path.exists(file_path):
        if display_callback:
            display_callback(f"Erreur : Le fichier {file_path} n'existe pas pour être écrasé.")
        return

    try:
        file_size = os.path.getsize(file_path)
        with open(file_path, 'wb') as file:
            file.write(b'\x00' * file_size)

        # Appeler le callback pour indiquer que le fichier a été écrasé
        if display_callback:
            display_callback(os.path.basename(file_path))
    except Exception as e:
        if display_callback:
            display_callback(f"Erreur lors de l'écrasement du fichier {file_path} : {e}")


def create_archive(directory, display_callback=None):
    print("create_archive called")
    if not os.path.exists(directory):
        if display_callback:
            display_callback(f"Erreur : le dossier {directory} n'existe pas.")
        return
    try:
        archive_path = shutil.make_archive(directory, 'zip', directory)
        if display_callback:
            display_callback(os.path.basename(archive_path))  # Affiche uniquement le nom
        return archive_path
    except Exception as e:
        if display_callback:
            display_callback(f"Erreur lors de la création de l'archive : {e}")
        return


def extract_archive(archive_path, extract_to=None):
    if not zipfile.is_zipfile(archive_path):
        print(f"Erreur : le fichier {archive_path} n'est pas un fichier zip.")
        return

    try:
        if extract_to is None:
            extract_to = os.path.splitext(archive_path)[0]  # Retirer ".zip"

        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)  # Extraction
            print(f"Archive extraite avec succès dans {extract_to}.")
        return extract_to
    except Exception as e:
        print(f"Erreur lors de la décompression de l'archive {archive_path} : {e}")
        return
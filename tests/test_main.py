import os

import pytest
from cryptography.fernet import Fernet

from my_package.file_crypto import encrypt_file, decrypt_file
from my_package.main import validate_file


@pytest.fixture
def generate_test_files(tmp_path):
    """Fixture pour générer plusieurs fichiers test."""
    file_1 = tmp_path / "file1.txt"
    file_2 = tmp_path / "file2.txt"
    file_1.write_text("Contenu de fichier 1")
    file_2.write_text("Contenu de fichier 2")
    return [file_1, file_2]  # Retourne les chemins des fichiers générés


@pytest.fixture
def encryption_key():
    """Fixture pour générer une clé de chiffrement."""
    return Fernet.generate_key()


def test_validate_multiple_files_exist(generate_test_files):
    """Test de validation pour plusieurs fichiers existants."""
    for file_path in generate_test_files:
        assert validate_file(str(file_path)) is True


def test_validate_multiple_files_missing(tmp_path):
    """Test pour vérifier qu'une liste contenant des fichiers inexistants échoue."""
    missing_file = tmp_path / "missing_file.txt"
    with pytest.raises(
            FileNotFoundError, match=f"Erreur : Le fichier '{missing_file}' n'existe pas."
    ):
        validate_file(str(missing_file))


def test_encrypt_multiple_files(tmp_path, generate_test_files, encryption_key):
    """Test du chiffrement de plusieurs fichiers."""
    for file_path in generate_test_files:
        encrypt_file(str(file_path), encryption_key)
        encrypted_file = str(file_path) + ".enc"
        assert os.path.exists(
            encrypted_file
        ), f"Le fichier chiffré '{encrypted_file}' est manquant."
        os.remove(encrypted_file)  # Nettoyage après test


def test_decrypt_multiple_files(tmp_path, generate_test_files, encryption_key):
    """Test du déchiffrement de plusieurs fichiers."""
    # Préparer les fichiers en les chiffrant d'abord
    encrypted_files = []
    for file_path in generate_test_files:
        encrypt_file(str(file_path), encryption_key)
        encrypted_file = str(file_path) + ".enc"
        encrypted_files.append(encrypted_file)
        os.remove(file_path)  # Simuler suppression des fichiers originaux

    # Déchiffrer les fichiers chiffrés
    for encrypted_file in encrypted_files:
        decrypt_file(str(encrypted_file), encryption_key)
        decrypted_file = encrypted_file.replace(".enc", "")
        assert os.path.exists(
            decrypted_file
        ), f"Le fichier déchiffré '{decrypted_file}' est manquant."
        os.remove(decrypted_file)  # Nettoyage après test
        os.remove(encrypted_file)  # Nettoyer aussi les fichiers chiffrés


def test_encrypt_missing_file(tmp_path, encryption_key):
    """Test pour vérifier l'erreur lorsque l'un des fichiers à chiffrer n'existe pas."""
    missing_file = tmp_path / "missing_file.txt"
    result = encrypt_file(str(missing_file), encryption_key)
    assert (
            result is None
    ), "encrypt_file devrait retourner None si le fichier n'existe pas."


def test_decrypt_non_encrypted_file(tmp_path, encryption_key):
    """Test pour vérifier qu'une tentative de déchiffrement d'un fichier non chiffré génère une erreur."""
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Texte non chiffré")
    result = decrypt_file(str(test_file), encryption_key)
    assert (
            result is None
    ), "decrypt_file devrait retourner None pour un fichier non chiffré."
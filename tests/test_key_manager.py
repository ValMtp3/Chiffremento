import os

import pytest
from cryptography.fernet import Fernet

from key_manager import generate_key, load_key


def test_generate_key_creates_file(tmp_path):
    key_file = tmp_path / "secret.key"
    os.chdir(tmp_path)  # Change directory to the temp path
    generate_key()
    assert key_file.exists() and key_file.is_file()


def test_generate_key_creates_valid_key(tmp_path):
    key_file = tmp_path / "secret.key"
    os.chdir(tmp_path)  # Change directory to the temp path
    generate_key()
    with open(key_file, "rb") as file:
        key = file.read()
    assert isinstance(key, bytes)
    assert len(key) > 0


def test_generate_key_overwrites_existing_key(tmp_path):
    key_file = tmp_path / "secret.key"
    os.chdir(tmp_path)  # Change directory to the temp path
    with open(key_file, "wb") as file:
        file.write(b"dummy_key")
    generate_key()
    with open(key_file, "rb") as file:
        new_key = file.read()
    assert new_key != b"dummy_key"


def test_load_key_successful(tmp_path):
    secret_key_path = tmp_path / "secret.key"
    test_key = Fernet.generate_key()
    with open(secret_key_path, "wb") as key_file:
        key_file.write(test_key)

    os.chdir(tmp_path)
    loaded_key = load_key()
    assert loaded_key == test_key


def test_load_key_file_not_found(tmp_path):
    os.chdir(tmp_path)
    with pytest.raises(FileNotFoundError):
        load_key()


def test_load_key_invalid_format(tmp_path):
    secret_key_path = tmp_path / "secret.key"
    with open(secret_key_path, "wb") as key_file:
        key_file.write(b"invalid_key_data")

    os.chdir(tmp_path)
    loaded_key = load_key()
    assert loaded_key == b"invalid_key_data"


def test_key_usage_success(tmp_path):
    secret_key_path = tmp_path / "secret.key"
    key = Fernet.generate_key()
    with open(secret_key_path, "wb") as key_file:
        key_file.write(key)

    os.chdir(tmp_path)
    loaded_key = load_key()
    cipher_suite = Fernet(loaded_key)

    # Chiffrer et déchiffrer un texte
    original_content = b"This is a test."
    encrypted_content = cipher_suite.encrypt(original_content)
    decrypted_content = cipher_suite.decrypt(encrypted_content)

    assert decrypted_content == original_content


def test_invalid_key_usage(tmp_path):
    secret_key_path = tmp_path / "secret.key"
    invalid_key = b"invalid_key_data_should_fail"
    with open(secret_key_path, "wb") as key_file:
        key_file.write(invalid_key)

    os.chdir(tmp_path)
    loaded_key = load_key()

    # Vérifier que Fernet rejette la clé invalide
    with pytest.raises(Exception):  # InvalidToken ou autre erreur dépendante
        cipher_suite = Fernet(loaded_key)

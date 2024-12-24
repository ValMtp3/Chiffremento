import os
import pytest
from cryptography.fernet import Fernet

from file_crypto import encrypt_file, decrypt_file, overwrite_file


@pytest.fixture
def encryption_key():
    """Fixture pour générer une clé de chiffrement."""
    return Fernet.generate_key()


@pytest.mark.parametrize(
    "file_name", ["nonexistent_file.txt", "another_missing_file.txt"]
)
def test_encrypt_file_nonexistent_file(tmp_path, encryption_key, file_name):
    """Tester le comportement de encrypt_file avec un fichier inexistant."""
    non_existent_file = tmp_path / file_name
    encrypt_file(str(non_existent_file), encryption_key)
    # Vérifie que le fichier chiffré n'est pas créé
    assert not os.path.exists(str(non_existent_file) + ".enc")


def test_encrypt_file_creates_encrypted_file(tmp_path, encryption_key):
    """Vérifie que encrypt_file crée correctement un fichier chiffré."""
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("This is a test.")

    encrypt_file(str(test_file), encryption_key)
    encrypted_file = str(test_file) + ".enc"

    # Assertions
    assert os.path.exists(encrypted_file)
    with open(encrypted_file, "rb") as f:
        encrypted_data = f.read()
    assert encrypted_data != b"This is a test."


def test_encrypt_decrypt_cycle(tmp_path, encryption_key):
    """Tester le cycle de chiffrement/déchiffrement pour vérifier l'intégrité des données."""
    test_file = tmp_path / "test_file.txt"
    original_content = "This is a test."
    test_file.write_text(original_content)

    # Chiffrement
    encrypt_file(str(test_file), encryption_key)
    encrypted_file = tmp_path / "test_file.txt.enc"
    assert encrypted_file.exists()

    # Déchiffrement
    decrypt_file(str(encrypted_file), encryption_key)
    decrypted_file = tmp_path / "test_file.txt"

    # Vérifie que les données sont récupérées intactes
    assert decrypted_file.exists()
    assert decrypted_file.read_text() == original_content


@pytest.mark.parametrize("file_name", ["nonexistent_file.enc", "missing_file.enc"])
def test_decrypt_file_nonexistent_file(tmp_path, encryption_key, file_name):
    """Vérifie que decrypt_file gère correctement un fichier chiffré inexistant."""
    non_existent_file = tmp_path / file_name
    assert decrypt_file(str(non_existent_file), encryption_key) is None


def test_decrypt_file_not_encrypted_extension(tmp_path, encryption_key):
    """Vérifie que decrypt_file échoue correctement avec un fichier non chiffré."""
    non_encrypted_file = tmp_path / "test_file.txt"
    non_encrypted_file.write_text("test content")
    assert decrypt_file(str(non_encrypted_file), encryption_key) is None


def test_decrypt_file_with_invalid_key(tmp_path, encryption_key):
    """Vérifie que decrypt_file échoue correctement avec une clé invalide."""
    valid_key = encryption_key
    invalid_key = Fernet.generate_key()
    cipher_suite = Fernet(valid_key)

    # Créer un fichier chiffré
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("This is a test.")

    encrypted_file = tmp_path / "test_file.txt.enc"
    with open(encrypted_file, "wb") as file:
        file.write(cipher_suite.encrypt(test_file.read_bytes()))

    # Tente de déchiffrer avec une clé invalide
    assert decrypt_file(str(encrypted_file), invalid_key) is None


def test_decrypt_file_success(tmp_path, encryption_key):
    """Vérifie le succès d'une opération de déchiffrement avec une clé valide."""
    cipher_suite = Fernet(encryption_key)

    original_file = tmp_path / "test_file.txt"
    original_content = b"This is a test."
    encrypted_file = tmp_path / "test_file.txt.enc"

    # Crée un fichier chiffré
    with open(original_file, "wb") as file:
        file.write(original_content)
    with open(encrypted_file, "wb") as file:
        file.write(cipher_suite.encrypt(original_content))

    # Déchiffrement
    decrypt_file(str(encrypted_file), encryption_key)

    # Vérifie que les données déchiffrées sont correctes
    decrypted_file = tmp_path / "test_file.txt"
    assert decrypted_file.exists()
    assert decrypted_file.read_bytes() == original_content


def test_overwrite_file_existing_file(tmp_path):
    """Vérifie que overwrite_file écrase bien un fichier existant."""
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("Sensitive data")

    file_size = file_path.stat().st_size
    overwrite_file(str(file_path))

    # Vérifie que le fichier a le même taille mais contient uniquement des zéros
    assert os.path.exists(file_path)
    with open(file_path, "rb") as file:
        content = file.read()
    assert content == b"\x00" * file_size


def test_overwrite_file_nonexistent_file(tmp_path, capsys):
    """Vérifie que overwrite_file gère correctement un fichier inexistant."""
    non_existent_file = tmp_path / "nonexistent_file.txt"

    overwrite_file(str(non_existent_file))

    # Capture la sortie standard
    captured = capsys.readouterr()
    assert "Erreur : Le fichier" in captured.out
    assert not os.path.exists(non_existent_file)


def test_overwrite_file_empty_file(tmp_path):
    """Vérifie que overwrite_file fonctionne avec un fichier vide."""
    empty_file = tmp_path / "empty_file.txt"
    empty_file.write_text("")  # Crée un fichier vide

    overwrite_file(str(empty_file))

    assert os.path.exists(empty_file)
    with open(empty_file, "rb") as file:
        content = file.read()
    assert content == b""  # Le fichier reste vide
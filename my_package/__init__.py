# __init__.py - Initialise le package pour Chiffremento

# Version du package
__version__ = "0.1"

from .db import get_database, save_key, get_key
from .file_crypto import (
    encrypt_file,
    decrypt_file,
    overwrite_file,
    create_archive,
    extract_archive,
)
# Importer les fonctions principales pour faciliter leur utilisation
from .key_manager import generate_key, load_key

# Nom du package pour identifier les logs ou autres utilisations
PACKAGE_NAME = "Chiffremento"
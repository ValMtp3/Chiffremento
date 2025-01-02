import os
from datetime import datetime

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI")


# Connexion à la bdd MongoDB
def get_database():
    try:
        client = MongoClient(DATABASE_URI)
        db = client["ChiffrementoDB"]
        return db
    except Exception as e:
        print(f"Erreur lors de la connexion à MongoDB : {e}")
        raise


# Enregistrer une clé privée chiffrée, clé publique et date de création dans MongoDB
def save_key(key_name, private_key, public_key):
    db = get_database()
    collection = db["UserKeys"]  # Nom de la collection
    key_document = {
        "nom": key_name,  # Nom ou identifiant de la clé
        "cle_privee_chiffree": private_key,  # Clé privée chiffrée
        "cle_publique": public_key,  # Clé publique
        "date_creation": datetime.now()  # Date de création
    }
    result = collection.insert_one(key_document)
    print(f"Clé enregistrée avec succès dans MongoDB avec l'ID : {result.inserted_id}")


# Charger une clé privée chiffrée et publique depuis la DB à partir du nom
def get_key(key_name):
    db = get_database()
    collection = db["UserKeys"]

    key_document = collection.find_one({"nom": key_name})  # Recherche par nom
    if key_document:
        return key_document
    else:
        raise ValueError(f"Clé '{key_name}' introuvable dans la base.")
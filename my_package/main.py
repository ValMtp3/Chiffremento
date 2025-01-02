import argparse
import os

from my_package.file_crypto import encrypt_file, decrypt_file, overwrite_file, create_archive, extract_archive
from my_package.key_manager import generate_key, load_key


def validate_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Erreur : Le fichier '{file_path}' n'existe pas.")
    return True


# Nouvelle fonction 'main' qui encapsule la logique principale
def main():
    # Création du parseur d'arguments pour la ligne de commande
    parser = argparse.ArgumentParser(description="Chiffrement et déchiffrement de fichiers")

    # Ajout des arguments attendus
    parser.add_argument("files", nargs="+", help="Chemin des fichiers à chiffrer ou à déchiffrer")
    parser.add_argument("action", choices=["encrypt", "decrypt"],
                        help="Action à effectuer : 'encrypt' pour chiffrer, 'decrypt' pour déchiffrer")
    parser.add_argument("--delete", action="store_true",
                        help="Supprime le(s) fichier(s) original(aux) après l'opération")

    # Analyse des arguments passés en ligne de commande
    args = parser.parse_args()

    # Récupération des valeurs des arguments
    file_paths = args.files
    action = args.action

    try:
        # Chargement ou génération de la clé depuis MongoDB
        try:
            key = load_key()
            print("Clé chargée avec succès depuis MongoDB.")
        except ValueError:
            print("Clé non trouvée dans MongoDB. Génération d'une nouvelle clé.")
            key = generate_key()
            print("Nouvelle clé générée et enregistrée dans MongoDB.")

        # Traiter chaque fichier passé en argument
        for file_path in file_paths:
            try:
                # Vérifier si le chemin pointe vers un dossier
                if os.path.isdir(file_path):
                    zip_path = create_archive(file_path)
                    if zip_path:
                        print(f"Dossier compressé avec succès : {os.path.basename(zip_path)}")
                        file_path = zip_path  # Utiliser l'archive pour les étapes suivantes
                    else:
                        print(f"Erreur : Impossible de compresser le dossier {os.path.basename(file_path)}")
                        continue

                # Valider que le fichier existe
                validate_file(file_path)

                # Exécuter l'action spécifiée
                if action == "encrypt":
                    encrypt_file(file_path, key)
                    print(f"Le fichier {os.path.basename(file_path)} a été chiffré avec succès.")
                elif action == "decrypt":
                    if file_path.endswith('.zip.enc'):
                        decrypt_file(file_path, key)

                        # Remplacer le suffixe .enc pour obtenir le fichier déchiffré
                        decrypted_zip = file_path.replace('.enc', '')

                        # Vérifier que le fichier déchiffré existe
                        if os.path.exists(decrypted_zip):
                            extract_dir = extract_archive(decrypted_zip)
                            if extract_dir:
                                if args.delete:
                                    os.remove(decrypted_zip)  # Supprimer l'archive déchiffrée
                            else:
                                print(f"Erreur : Impossible de décompresser {decrypted_zip}.")
                        else:
                            print(f"Erreur : Le fichier déchiffré {decrypted_zip} est introuvable.")
                    else:
                        print(f"Déchiffrement du fichier {os.path.basename(file_path)} en cours...")
                        decrypt_file(file_path, key)
                        print(f"Le fichier {os.path.basename(file_path)} a été déchiffré.")

                # Supprimer le fichier original si l'option --delete a été spécifiée
                if args.delete:
                    overwrite_file(file_path)
                    os.remove(file_path)
                    print(f"Le fichier original {os.path.basename(file_path)} a été supprimé.")

            except FileNotFoundError as e:
                print(f"Erreur : {e}")
            except Exception as e:
                print(f"Une erreur inattendue s'est produite : {e}")

    except Exception as e:
        print(f"Une erreur globale s'est produite : {e}")


# Appel de la fonction 'main' uniquement lorsqu'exécuté directement
if __name__ == "__main__":
    main()
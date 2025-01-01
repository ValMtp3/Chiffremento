# Documentation du projet : Chiffremento

Bienvenue dans **Chiffremento**, une application Python simple et sécurisée permettant de chiffrer, déchiffrer, et gérer
des fichiers de manière sécurisée. Cette application utilise la bibliothèque **cryptography** pour assurer une sécurité
optimale lors du traitement des fichiers sensibles.

---

## Table des matières

- [Aperçu](#aperçu)
- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [Limitations](#limitations)
- [Contributeurs](#contributeurs)

---

## Aperçu

**File Encryptor** utilise l'algorithme [Fernet](https://cryptography.io/en/latest/fernet/) pour garantir le chiffrement
et le déchiffrement sûrs des fichiers. L'objectif principal est de sécuriser les données en toute simplicité tout en
offrant des outils fiables pour supprimer les fichiers originaux après traitement afin d'éviter tout accès non autorisé.

## Fonctionnalités

- **Chiffrement** des fichiers en utilisant une clé forte générée automatiquement.
- **Compression et chiffrement des dossiers** : Compressez tout un dossier au format zip et chiffrez-le de manière
  sécurisée.
- **Déchiffrement** des fichiers chiffrés à l'aide de la clé correspondante.
- **Suppression sécurisée** des fichiers originaux après chiffrement ou déchiffrement.
- **Gestion de clé** sécurisée : génération, sauvegarde et chargement automatique des clés.

---

## Installation

Avant de commencer, assurez-vous d'avoir Python 3.13 ou une version ultérieure installée sur votre machine.

### Étapes d'installation

1. Clonez ce dépôt ou téléchargez les fichiers du projet :

```shell script
git clone https://github.com/ValMtp3/Chiffremento
```

2. Installez les dépendances :

```shell script
pip install -r requirements.txt
```

3. Vérifiez la configuration de la clé :
    - **Pas de clé existante** : Une clé est générée automatiquement et sauvegardée dans un fichier nommé `secret.key`
      lors de la première exécution.
    - **Fichier `secret.key` existant** : La clé sera automatiquement chargée depuis ce fichier.

---

## Utilisation

### Exécution de l'application

L'application est exécutée à l'aide de la ligne de commande. Utilisez les arguments suivants pour effectuer une
opération sur des fichiers ou des dossiers.

#### Syntaxe générale :

```shell script
python main.py <CHEMIN_DES_FICHIERS_OU_DOSSIER> <ACTION> [OPTIONS]
```

### Arguments obligatoires :

- `<CHEMIN_DES_FICHIERS_OU_DOSSIER>` : Liste des fichiers ou dossiers à traiter (chemins relatifs ou absolus).
- `<ACTION>` : Action à effectuer, soit `encrypt` pour chiffrer des fichiers, soit `decrypt` pour les déchiffrer.
- `<ACTION>` : Action à effectuer, soit `encrypt` pour chiffrer des fichiers ou des dossiers compressés, soit `decrypt`
  pour les déchiffrer.

### Options :

- `--delete` : Supprime les fichiers originaux de manière sécurisée après le chiffrement ou le déchiffrement.

#### Exemple d'utilisation :

1. **Chiffrer un fichier :**

```shell script
python main.py mon_fichier.txt encrypt
```

Résultat : Le fichier `mon_fichier.txt` sera converti en un fichier chiffré nommé `mon_fichier.txt.enc`.

2. **Chiffrer tout un dossier :**

```shell script
python main.py mon_dossier encrypt
```

Résultat : Le dossier `mon_dossier` sera compressé en `mon_dossier.zip` et chiffré en `mon_dossier.zip.enc`.

```shell script
python main.py mon_fichier.txt encrypt
```

Résultat : Le fichier `mon_fichier.txt` sera converti en un fichier chiffré nommé `mon_fichier.txt.enc`.

2. **Déchiffrer un fichier :**

```shell script
python main.py mon_fichier.txt.enc decrypt
```

Résultat : Le fichier chiffré `mon_fichier.txt.enc` sera restauré sous son nom d'origine (`mon_fichier.txt`).

3. **Chiffrer un fichier et supprimer l'original :**

```shell script
python main.py mon_fichier.txt encrypt --delete
```

Résultat : Le fichier `mon_fichier.txt` sera chiffré, et l'original sera supprimé de manière sécurisée.

4. **Déchiffrer plusieurs fichiers ou un dossier compressé chiffré :**

```shell script
python main.py fichier1.enc fichier2.enc decrypt
python main.py mon_dossier.zip.enc decrypt
```

---

## Structure du projet

Voici une description des fichiers principaux du projet :

- **`main.py`** : Point d'entrée de l'application. Gère les arguments de la ligne de commande et exécute les actions (
  chiffrement, déchiffrement, compression, suppression).
- **`file_crypto.py`** : Contient les fonctions principales pour chiffrer, déchiffrer et écraser les fichiers.
    - `encrypt_file(file_path, key)` : Chiffre un fichier donné.
    - `encrypt_folder(folder_path, key)` : Compresse et chiffre un dossier donné.
    - `decrypt_file(file_path, key)` : Déchiffre un fichier donné.
    - `overwrite_file(file_path)` : Écrase le contenu d'un fichier avant sa suppression.
- **`key_manager.py`** : Gère la génération et le chargement des clés de chiffrement.
    - `generate_key()` : Génère une clé de chiffrement sécurisée.
    - `load_key()` : Charge une clé existante.
- **`requirements.txt`** : Décrit les dépendances nécessaires au projet.

---

## Limitations

- **Compatibilité limitée** : Bien que les dossiers puissent être compressés et chiffrés, l'application ne prend pas en
  charge les volumes de données extrêmement volumineux (> 1 Go).
- **Dépendance à `secret.key`** : La clé de chiffrement doit être conservée en lieu sûr pour éviter les pertes de
  données.
- **Vérifications de type de fichier** : L'application ne vérifie pas l'intégrité ou le format des fichiers.
  Assurez-vous de manipuler uniquement des fichiers pris en charge.

---

## Contributeurs

Créé par **@ValMtp3**.

N'hésitez pas à soumettre des améliorations ou rapports de bugs en ouvrant
une [issue](https://github.com/votre-repo/issues) ou une pull request.

Bon chiffrement! 🎉
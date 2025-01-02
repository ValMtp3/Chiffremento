from setuptools import setup, find_packages

setup(
    name="Chiffremento",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pymongo>=4.10.1",
        "cryptography>=44.0.0",
    ],
    entry_points={
        'console_scripts': [
            'chiffremento=my_package.main:main',
        ],
    },
    author="Valentin Fiess",  # Nom de l'auteur
    description="Un projet de chiffrement et de déchiffrement de fichiers et dossier utilisant MongoDB",
    url="https://github.com/ValMtp3/Chiffremento",  # Lien vers un dépôt GitHub (facultatif)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
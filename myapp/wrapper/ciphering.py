"""Module pour le chiffrement et déchiffrement des secrets avec GnuPG."""

import os
import subprocess
from dotenv import load_dotenv


def encrypt_secret(secret: str) -> bytes:
    """
    Chiffre un secret avec GnuPG en mode symétrique.
    Retourne les données chiffrées sous forme binaire.

    Args:
        secret (str): Le secret à chiffrer.

    Returns:
        bytes: Les données chiffrées sous forme binaire.
    """
    load_dotenv()
    gpg_passphrase = os.getenv("GPG_PASSPHRASE")

    result = subprocess.run(
        ["gpg", "--batch", "--yes", "--passphrase", gpg_passphrase, "--symmetric"],
        input=secret.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        raise ValueError(f"Erreur de chiffrement : {result.stderr.decode()}")

    return result.stdout


def decrypt_secret(encrypted_secret: bytes) -> str:
    """
    Déchiffre un secret chiffré avec GnuPG en mode symétrique.
    Retourne le secret en clair.

    Args:
        encrypted_secret (bytes): Le secret chiffré à déchiffrer.

    Returns:
        str: Le secret déchiffré en clair.
    """
    load_dotenv()
    gpg_passphrase = os.getenv("GPG_PASSPHRASE")

    result = subprocess.run(
        ["gpg", "--batch", "--yes", "--passphrase", gpg_passphrase, "--decrypt"],
        input=encrypted_secret,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        raise ValueError(f"Erreur de déchiffrement : {result.stderr.decode()}")

    return result.stdout.decode()

from cryptography.fernet import Fernet

def generate_key():
    """
    Generate a Fernet encryption key.
    Returns a URL-safe base64-encoded 32-byte key.
    """
    return Fernet.generate_key().decode('utf-8')
from cryptography.fernet import Fernet
import base64

def encrypt_file(file_bytes: bytes, key: str) -> bytes:
    """
    Encrypt file bytes using Fernet encryption.
    
    Args:
        file_bytes: The raw bytes of the file to encrypt
        key: The encryption key (must be a valid Fernet key)
    
    Returns:
        Encrypted bytes
    """
    # Ensure key is in bytes format
    if isinstance(key, str):
        key = key.encode('utf-8')
    
    # Create Fernet instance
    fernet = Fernet(key)
    
    # Encrypt the file bytes
    encrypted_data = fernet.encrypt(file_bytes)
    
    return encrypted_data
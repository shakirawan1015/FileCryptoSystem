from cryptography.fernet import Fernet

def decrypt_file(file_data, key):

    fernet = Fernet(key)

    decrypted_data = fernet.decrypt(file_data)

    return decrypted_data
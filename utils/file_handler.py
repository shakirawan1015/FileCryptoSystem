import os

def save_file(file_content, file_name, save_directory):
    """
    Save uploaded file to specified directory
    """
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    file_path = os.path.join(save_directory, file_name)
    
    with open(file_path, 'wb') as f:
        f.write(file_content)
    
    return file_path

def delete_file(file_path):
    """
    Delete file from specified path
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False
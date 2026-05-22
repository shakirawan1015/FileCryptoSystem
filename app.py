import streamlit as st
import sys
import os

# Import utilities from the utils folder
from utils.encryption import encrypt_file
from utils.decryption import decrypt_file
from utils.key_generator import generate_key
from utils.file_handler import save_file, delete_file

# Page configuration
st.set_page_config(page_title="File Encryption System", layout="wide")

# Custom CSS to add space between tabs
st.markdown("""
<style>
    div[data-testid="stTabs"] {
        gap: 20px;
    }
    div[data-testid="stTab"] {
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

# Main App Title
st.title("File Encryption System")

# Create tabs - Generate Key comes FIRST
tab_generate, tab_encrypt, tab_decrypt = st.tabs(["🔑 Generate Key", "🔒 Encrypt File", "🔓 Decrypt File"])

# -----------------------------------------------------------------------------
# TAB 1: GENERATE KEY (NOW FIRST)
# -----------------------------------------------------------------------------
with tab_generate:
    st.subheader("🔑 Encryption Key Generator")
    st.caption("Generate a secure random encryption key for your files.")
    st.write("")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Generate New Key")
        st.write("Click the button below to generate a secure random key.")
        
        if st.button("🔑 Generate Secure Key", use_container_width=True, type="primary"):
            try:
                new_key = generate_key()
                st.session_state['generated_key'] = new_key
                st.success("Key generated successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error generating key: {str(e)}")
    
    with col2:
        if 'generated_key' in st.session_state:
            st.markdown("### Your Generated Key")
            st.code(st.session_state['generated_key'], language="text")
            
            st.info("⚠️ **Important:** Save this key in a secure place. You'll need it to decrypt your files!")
            
            # Download button for the generated key
            st.download_button(
                label="⬇️ Download Key File",
                data=st.session_state['generated_key'].encode('utf-8'),
                file_name="secret_key.key",
                mime="text/plain",
                use_container_width=True,
                type="secondary"
            )
        else:
            st.markdown("### Your Generated Key")
            st.info("Click 'Generate Secure Key' to create a new encryption key.")

# -----------------------------------------------------------------------------
# TAB 2: ENCRYPT FILE
# -----------------------------------------------------------------------------
with tab_encrypt:
    st.subheader("🔒 Encrypt Any File")
    st.caption("Upload your file, enter your secret key, and download the encrypted version instantly.")
    st.write("")

    # Layout using columns
    col1, col2 = st.columns([1.1, 0.9], gap="large")

    with col1:
        uploaded_file = st.file_uploader(
            "Select file to encrypt",
            help="Upload documents, pictures, videos, or any other file."
        )

    with col2:
        key_input = st.text_input(
            "Enter Encryption Key",
            type="password",
            placeholder="Paste your secret key here...",
            key="encrypt_key_input",
            help="Enter your secret key or generate a new one in the 'Generate Key' tab"
        )
        
        # Add a button to generate a new key
        if st.button("🔑 Generate New Key", key="gen_key_btn_encrypt"):
            try:
                new_key = generate_key()
                st.session_state['generated_key'] = new_key
                st.success("Key generated! Check the 'Generate Key' tab to copy it.")
                st.rerun()
            except Exception as e:
                st.error(f"Error generating key: {str(e)}")

    # Display file metadata if uploaded
    if uploaded_file:
        st.write("---")
        st.markdown(f"**File Selected:** `{uploaded_file.name}`")
        file_size_kb = uploaded_file.size / 1024
        st.markdown(f"**File Size:** `{file_size_kb:.2f} KB`")

    # Initialize session state for encrypted data
    if 'encrypted_data' not in st.session_state:
        st.session_state.encrypted_data = None
    if 'encryption_error' not in st.session_state:
        st.session_state.encryption_error = None

    if uploaded_file and key_input:
        # Create a form to handle Enter key press
        with st.form(key="encrypt_form"):
            st.write("")  # Empty write to maintain spacing
            submit_encrypt = st.form_submit_button(
                label='🔒 Start Encryption', 
                use_container_width=True, 
                type="primary"
            )
            
            # Logic to execute when the button is clicked
            if submit_encrypt:
                with st.spinner("Encrypting file..."):
                    try:
                        # Read the uploaded file
                        file_bytes = uploaded_file.read()
                        
                        # Call the encryption utility function
                        encrypted_data = encrypt_file(file_bytes, key_input)
                        
                        # Store in session state
                        st.session_state.encrypted_data = encrypted_data
                        st.session_state.encryption_error = None
                        st.success("Encryption successful!")
                        
                    except Exception as e:
                        st.session_state.encrypted_data = None
                        st.session_state.encryption_error = f"Error during encryption: {str(e)}"
                        st.error(st.session_state.encryption_error)

    # Show download button OUTSIDE the form
    if st.session_state.encrypted_data is not None and uploaded_file:
        st.download_button(
            label="⬇️ Download Encrypted File",
            data=st.session_state.encrypted_data,
            file_name=f"encrypted_{uploaded_file.name}",
            mime="application/octet-stream",
            use_container_width=True,
            type="primary"
        )
    
    elif uploaded_file and not key_input:
        st.warning("Please enter a secret key to proceed or generate a new one.")

# -----------------------------------------------------------------------------
# TAB 3: DECRYPT FILE
# -----------------------------------------------------------------------------
with tab_decrypt:
    st.subheader("🔓 Decrypt File")
    st.caption("Upload an encrypted file and enter the secret key to decrypt it.")
    st.write("")
    
    col1, col2 = st.columns([1.1, 0.9], gap="large")
    
    with col1:
        upload_decrypt = st.file_uploader(
            "Select encrypted file to decrypt",
            help="Upload the encrypted file you want to decrypt"
        )
    
    with col2:
        decrypt_key = st.text_input(
            "Enter Decryption Key",
            type="password",
            placeholder="Paste your secret key here...",
            key="decrypt_key_input",
            help="Enter the same key used for encryption"
        )
    
    # Display file metadata if uploaded
    if upload_decrypt:
        st.write("---")
        st.markdown(f"**File Selected:** `{upload_decrypt.name}`")
        file_size_kb = upload_decrypt.size / 1024
        st.markdown(f"**File Size:** `{file_size_kb:.2f} KB`")

    # Initialize session state for decrypted data
    if 'decrypted_data' not in st.session_state:
        st.session_state.decrypted_data = None
    if 'decryption_error' not in st.session_state:
        st.session_state.decryption_error = None

    if upload_decrypt and decrypt_key:
        with st.form(key="decrypt_form"):
            st.write("")
            submit_decrypt = st.form_submit_button(
                "🔓 Start Decryption",
                use_container_width=True,
                type="primary"
            )
            
            if submit_decrypt:
                with st.spinner("Decrypting file..."):
                    try:
                        # Read the uploaded file
                        encrypted_bytes = upload_decrypt.read()
                        
                        # Call the decryption utility function
                        decrypted_data = decrypt_file(encrypted_bytes, decrypt_key)
                        
                        # Store in session state
                        st.session_state.decrypted_data = decrypted_data
                        st.session_state.decryption_error = None
                        st.success("Decryption successful!")
                        
                    except Exception as e:
                        st.session_state.decrypted_data = None
                        st.session_state.decryption_error = f"Decryption failed: {str(e)}"
                        st.error(st.session_state.decryption_error)
    
    # Show download button OUTSIDE the form
    if st.session_state.decrypted_data is not None and upload_decrypt:
        # Remove 'encrypted_' prefix if it exists
        original_name = upload_decrypt.name
        if original_name.startswith('encrypted_'):
            original_name = original_name[10:]
        
        st.download_button(
            label="⬇️ Download Decrypted File",
            data=st.session_state.decrypted_data,
            file_name=original_name,
            mime="application/octet-stream",
            use_container_width=True,
            type="primary"
        )
    
    elif upload_decrypt and not decrypt_key:
        st.warning("Please enter the decryption key to proceed.")
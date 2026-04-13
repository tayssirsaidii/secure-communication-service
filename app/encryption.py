import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
# Path where the secret key will be stored
KEY_PATH = "keys/secret.key"
# Load existing key or generate a new one if it doesn't exist or is invalid
def load_or_generate_key():
    # Check if key file exists and has valid length
    if os.path.exists(KEY_PATH):
        with open(KEY_PATH, "rb") as f:
            key = f.read()
          # Check if key length is valid (must be 16, 24, or 32 bytes)
        if len(key) not in (16, 24, 32):
            print(f"Invalid key length {len(key)} bytes detected, regenerating key...")
            # Generate a new 256-bit key (32 bytes)
            key = AESGCM.generate_key(bit_length=256)
            with open(KEY_PATH, "wb") as f:
                f.write(key)
    else:
            # Create the 'keys' directory if it doesn't exist
        os.makedirs(os.path.dirname(KEY_PATH), exist_ok=True)
             # Generate a new 256-bit key (32 bytes)
        key = AESGCM.generate_key(bit_length=256)
         # Save the key to the file
        with open(KEY_PATH, "wb") as f:
            f.write(key)
    return key
# Load or generate the key
key = load_or_generate_key()

def encrypt_bytes(data: bytes) -> bytes:
      # Initialize AES-GCM cipher with the key
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)   # Generate a 12-byte random nonce
    ciphertext = aesgcm.encrypt(nonce, data, None)
    return nonce + ciphertext   # Prepend nonce to ciphertext for use during decryption

def decrypt_bytes(encrypted_data: bytes) -> bytes:
    aesgcm = AESGCM(key)  # Initialize AES-GCM cipher with the key
    nonce = encrypted_data[:12] # Extract the first 12 bytes as nonce
    ciphertext = encrypted_data[12:]# The rest is the ciphertext
    return aesgcm.decrypt(nonce, ciphertext, None)    # Decrypt the data 

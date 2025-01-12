import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

KEY_DIR = "keys"
PRIVATE_KEY_PATH = os.path.join(KEY_DIR, "private_key.pem")
PUBLIC_KEY_PATH = os.path.join(KEY_DIR, "public_key.pem")


def generate_or_load_keys():
    if not os.path.exists(KEY_DIR):
        os.makedirs(KEY_DIR)

    if not os.path.exists(PRIVATE_KEY_PATH) or not os.path.exists(PUBLIC_KEY_PATH):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        # Save private key
        with open(PRIVATE_KEY_PATH, "wb") as private_file:
            private_file.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )

        # Save public key
        with open(PUBLIC_KEY_PATH, "wb") as public_file:
            public_file.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )

    else:
        with open(PRIVATE_KEY_PATH, "rb") as private_file:
            private_key = serialization.load_pem_private_key(
                private_file.read(), password=None
            )
        with open(PUBLIC_KEY_PATH, "rb") as public_file:
            public_key = serialization.load_pem_public_key(public_file.read())

    return private_key, public_key

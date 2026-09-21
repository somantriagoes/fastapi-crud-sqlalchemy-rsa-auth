from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
import base64

with open("storage/rsa/private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )


def decrypt_password(encrypted):
    if encrypted is None:
        raise ValueError("Password is required")

    value = encrypted.encode() if isinstance(encrypted, str) else encrypted

    if isinstance(value, (bytes, bytearray)):
        try:
            decoded = base64.b64decode(value, validate=True)
        except (TypeError, ValueError):
            return value.decode("utf-8")

        if len(decoded) == 256:
            try:
                return private_key.decrypt(decoded, padding.PKCS1v15()).decode("utf-8")
            except ValueError:
                pass

        return value.decode("utf-8")

    return str(encrypted)
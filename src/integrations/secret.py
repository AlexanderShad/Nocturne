# secret.py

from gi.repository import Secret
import hashlib, secrets, string
from ..constants import FALLBACK_PASSWORD_PATH

BASE_SCHEMA = Secret.Schema.new(
    "com.jeffser.Nocturne.Password",
    Secret.SchemaFlags.NONE,
    {
        "type": Secret.SchemaAttributeType.STRING
    }
)

def keyring_available() -> bool:
    try:
        service = Secret.Service.get_sync(Secret.ServiceFlags.NONE, None)
        return bool(service)
    except Exception as e:
        pass
    return False

def store_password(password:str):
    if keyring_available():
        attributes = {"type": "password"}

        Secret.password_store_sync(
            BASE_SCHEMA,
            attributes,
            Secret.COLLECTION_DEFAULT,
            "Nocturne Login",
            password,
            None
        )
    else:
        with open(FALLBACK_PASSWORD_PATH, 'w') as f:
            f.write(password)

def get_hashed_password() -> tuple:
    # returns salt, hashed password
    password = ""
    if keyring_available():
        attributes = {"type": "password"}

        password = Secret.password_lookup_sync(
            BASE_SCHEMA,
            attributes,
            None
        )
    else:
        with open(FALLBACK_PASSWORD_PATH, 'r') as f:
            password = f.read()

    salt = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
    salted_password = password + salt

    hashed_password = hashlib.md5(salted_password.encode('utf-8')).hexdigest()

    return salt, hashed_password


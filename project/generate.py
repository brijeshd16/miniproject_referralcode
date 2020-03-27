import secrets

def generate_key():
    key = secrets.token_hex(5)

    return key
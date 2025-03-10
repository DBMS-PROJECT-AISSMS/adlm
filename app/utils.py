from app import bcrypt

def hash_text(text):
    return bcrypt.generate_password_hash(text).decode("utf-8")

def check_hash(hashed_text, plain_text):
    return bcrypt.check_password_hash(hashed_text, plain_text)
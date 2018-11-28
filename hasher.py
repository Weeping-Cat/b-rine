import hashlib
import uuid

def hash(password, salt):
    password = str(password).encode()
    passalt = password+salt.encode()
    hashed_password = hashlib.sha512(passalt).hexdigest()
    return hashed_password

def create_salt():
    salt = uuid.uuid4().hex
    return salt
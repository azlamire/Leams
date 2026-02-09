import bcrypt
import string
import random


# TODO: Make bcrypt func more powerful in core folder
def hash_password(clean_pass):
    bytes = clean_pass.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = str(bcrypt.hashpw(bytes.decode("utf-8"), salt))
    return hashed

def generate_stream_key():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=64)) # k = len of str
    stream_id = f"live_{random_string}"
    return stream_id

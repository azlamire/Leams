import bcrypt


# TODO: Make bcrypt func more powerful in core folder
def hash_password(clean_pass):
    bytes = clean_pass.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = str(bcrypt.hashpw(bytes.decode("utf-8"), salt))
    return hashed

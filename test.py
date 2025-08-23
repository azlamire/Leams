from datetime import timedelta

SECRET_KEY = open("jwt-private.pem").read()
print(SECRET_KEY,timedelta(minutes=30))

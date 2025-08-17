from models.user import UserSchema
from jwt_test import hash_password

john = UserSchema(
    username="john_doe",
    password=hash_password("securepassword123"),
    email="john@example.com"
)
from jwt import encode, decode
from utils.settings import Settings

settings = Settings()

def create_token(data: dict) -> str:
    token: str = encode(payload=data, key=settings.jwt_secret_key, algorithm="HS256")

    return token

def validate_token(token: str) -> dict:
    data: dict = decode(token, key=settings.jwt_secret_key, algorithms=['HS256'])

    return data
import os

from pydantic import BaseSettings
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    
    db_user: str            = os.getenv('PG_USER')
    db_pass: str            = os.getenv('PG_PASSWORD')
    db_host: str            = os.getenv('PG_HOST')
    db_port: str            = os.getenv('PG_PORT')
    db_name: str            = os.getenv('PG_DATABASE')

    jwt_secret_key: str     = os.getenv('JWT_SECRET_KEY')
    jwt_token_expire: int   = os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES')

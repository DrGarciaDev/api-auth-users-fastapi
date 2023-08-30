from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from utils.settings import Settings

settings = Settings()


# print(user)

database_url = f'postgresql://{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/{settings.db_name}'

# representa el motor de la base de datos, con el comando “echo=True” para que al momento de realizar la base de datos,
# me muestre por consola lo que esta realizando, que seria el codigo
engine = create_engine(database_url, echo=True)

# Se crea session para conectarse a la base de datos, se enlaza con el comando “bind” y se iguala a engine
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Sirve para manipular todas las tablas de la base de datos
Base = declarative_base()

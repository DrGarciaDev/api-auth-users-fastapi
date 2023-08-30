from fastapi import APIRouter, status, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
import bcrypt

# modulos locales 
from schemas.auth_schema import AuthLoginUserRequestSchema, AuthRegisterUserRequestSchema, AuthRegisterUserResponseSchema
from utils.jwt_manager import create_token
from services.auth_service import AuthService
from config.database import SessionLocal


auth_router = APIRouter(
    prefix='/api/auth',
    tags=['Auth']
)

@auth_router.post(path='/login', response_model=dict, status_code=status.HTTP_200_OK)
def login(user: AuthLoginUserRequestSchema = Body(...)):
    db = SessionLocal()
    usuario_registrado = AuthService(db).get_user_by_email(user.email)

    if not usuario_registrado:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Email no registrado')
    
    password_equals = bcrypt.checkpw(user.password.encode(), usuario_registrado['user'].password.encode())

    if password_equals:
        # print(jsonable_encoder(usuario_registrado))
        response = {
            # "token": create_token(user.dict())
            "token": create_token(jsonable_encoder(usuario_registrado))
        }
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No coincide el password')

    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


@auth_router.post(path='/register-user', response_model=AuthRegisterUserResponseSchema, status_code=status.HTTP_201_CREATED)
def register_user(user: AuthRegisterUserRequestSchema):
    # Debemos tenerla como bytes
    
    pass_codificado = user.password.encode()

    # La sal, necesaria para preparar nuestra contraseña, recomendado el 12
    sal = bcrypt.gensalt(12)

    # Hashear
    pass_hasheado = bcrypt.hashpw(pass_codificado, sal)
   
    user.password = pass_hasheado.decode()

    db = SessionLocal()
    new_user = AuthService(db).register_user(user=user)

    if not new_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Algo salió mal')
    
    user_json = jsonable_encoder(new_user)

    try:
        del user_json['password']
    except KeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Llave password no está en el diccionario')

    return JSONResponse(content=user_json, status_code=status.HTTP_201_CREATED)

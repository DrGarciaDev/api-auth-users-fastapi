from fastapi import APIRouter, status, Path, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
import bcrypt

# modulos locales 
from config.database import SessionLocal
from schemas.user_schema import UserSchema
from services.user_service import UserService
from middlewares.jwt_bearer import JWTBearer


user_router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@user_router.get(path='/get-all-users', response_model=List[UserSchema], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_all_users():
    db = SessionLocal()
    registros = UserService(db=db).get_users()

    return JSONResponse(content=jsonable_encoder(registros), status_code=status.HTTP_200_OK)

@user_router.get(path='/get-user/{id}', response_model=UserSchema, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_user(id: int = Path(ge=1, le=2000)):
    db = SessionLocal()
    registro = UserService(db).get_user(id=id)

    if not registro:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No encontrado"})
        
    return JSONResponse(content=jsonable_encoder(registro), status_code=status.HTTP_200_OK)


@user_router.post(path='/create-user', response_model=UserSchema, status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer())])
def create_user(user: UserSchema):
    # Debemos tenerla como bytes
    
    pass_texto_plano = user.password.encode()

    # La sal, necesaria para preparar nuestra contraseña
    sal = bcrypt.gensalt(12)

    # Hashear
    pass_hasheada = bcrypt.hashpw(pass_texto_plano, sal)
    print(str(pass_hasheada.decode()))
    user.password = str(pass_hasheada.decode())

    db = SessionLocal()
    new_user = UserService(db).create_user(user=user)

    return JSONResponse(content=jsonable_encoder(new_user), status_code=status.HTTP_201_CREATED)


@user_router.put(path='/update-user/{id}', response_model=dict, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def update_user(id:  int, user: UserSchema) -> dict:
    db = SessionLocal()
    registro = UserService(db=db).get_user(id=id)

    if not registro:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Registro no encontrado"})

    registro_editado = UserService(db).update_user(id=id, data=user)

    if not registro_editado:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Error al editar"})
    
    registro = UserService(db=db).get_user(id=id)
    print(registro)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Editado", "registro": jsonable_encoder(registro)})

@user_router.delete(path='/delete-user/{id}', response_model=dict, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def delete_user(id: int) -> dict:
    db = SessionLocal()
    registro = UserService(db=db).get_user(id=id)

    if not registro:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Registro No encontrado"})

    registro_eliminado = UserService(db=db).delete_user(id=id)
    
    if not registro_eliminado:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Error al eliminar"})
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Eliminado", "registro": jsonable_encoder(registro)})


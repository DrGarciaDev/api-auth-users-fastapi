from fastapi import APIRouter, status, Path, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

# modulos locales 
from config.database import SessionLocal
from schemas.user_roles_schema import UserRolesSchema
from services.user_roles_service import UserRolesService
from services.user_service import UserService
from services.role_service import RoleService
from middlewares.jwt_bearer import JWTBearer


user_roles_router = APIRouter(
    prefix='/users-roles',
    tags=['Users Roles']
)

@user_roles_router.post(path='/assing-role-to-user', response_model=dict, status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer())])
def assing_role_to_user(user_role: UserRolesSchema):
    
    db = SessionLocal()
    
    exist_user = UserService(db=db).get_user(id=user_role.user_id)

    if not exist_user:
        return JSONResponse(content={'message': 'No existe el usuario a asignarle el rol'}, status_code=status.HTTP_404_NOT_FOUND)

    exist_role = RoleService(db=db).get_role(id=user_role.role_id)

    if not exist_role:
        return JSONResponse(content={'message': 'No existe el rol para asignarle al usuario'}, status_code=status.HTTP_404_NOT_FOUND)
    
    exist_new_user_role = UserRolesService(db=db).get_exist_user_role(user_id=user_role.user_id, role_id=user_role.role_id)

    if exist_new_user_role:
        return JSONResponse(content={'message': 'El rol ya está asignado'}, status_code=status.HTTP_202_ACCEPTED)

    new_user_role = UserRolesService(db=db).assing_role_to_user(user_role=user_role)

    return JSONResponse(content=jsonable_encoder(new_user_role), status_code=status.HTTP_201_CREATED)

@user_roles_router.put(path='/reassing-role-to-user/{id}', response_model=dict, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def update_user(id:  int, user_role: UserRolesSchema) -> dict:
    
    db = SessionLocal()
    registro = UserRolesService(db=db).get_user_role(id=id)

    if not registro:
        return JSONResponse(content={"message": "Registro no encontrado"}, status_code=status.HTTP_404_NOT_FOUND)

    exist_user = UserService(db=db).get_user(id=user_role.user_id)

    if not exist_user:
        return JSONResponse(content={'message': 'No existe el usuario a asignarle el rol'}, status_code=status.HTTP_404_NOT_FOUND)

    exist_role = RoleService(db=db).get_role(id=user_role.role_id)

    if not exist_role:
        return JSONResponse(content={'message': 'No existe el rol para asignarle al usuario'}, status_code=status.HTTP_404_NOT_FOUND)
    
    exist_new_user_role = UserRolesService(db=db).get_exist_user_role(user_id=user_role.user_id, role_id=user_role.role_id)

    if exist_new_user_role:
        return JSONResponse(content={'message': 'El rol ya está asignado'}, status_code=status.HTTP_202_ACCEPTED)

    registro_editado = UserRolesService(db).update_user_role(id=id, data=user_role)

    if not registro_editado:
        return JSONResponse(content={"message": "Error al editar"}, status_code=status.HTTP_400_BAD_REQUEST)

    return JSONResponse(content={"message": "Editado", "registro": jsonable_encoder(registro_editado)}, status_code=status.HTTP_200_OK)

@user_roles_router.delete(path='/delete-user-role/{id}', response_model=dict, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def delete_user(id: int) -> dict:

    db = SessionLocal()
    registro = UserRolesService(db=db).get_user_role(id=id)

    if not registro:
        return JSONResponse(content={"message": "Registro No encontrado"}, status_code=status.HTTP_404_NOT_FOUND)

    registro_eliminado = UserRolesService(db=db).delete_user_role(id=id)
    
    if not registro_eliminado:
        return JSONResponse(content={"message": "Error al eliminar"}, status_code=status.HTTP_400_BAD_REQUEST)
    
    return JSONResponse(content={"message": "Eliminado", "registro": jsonable_encoder(registro)}, status_code=status.HTTP_200_OK)

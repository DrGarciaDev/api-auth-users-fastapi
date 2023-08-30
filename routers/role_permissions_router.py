from fastapi import APIRouter, status, Path, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

# modulos locales 
from config.database import SessionLocal
from schemas.role_permissions_schema import RolesPermissionsSchema
from services.role_permissions_service import RolePermissionsService
from services.role_service import RoleService
from services.permission_service import PermissionService
from middlewares.jwt_bearer import JWTBearer


role_permissions_router = APIRouter(
    prefix='/roles-permissions',
    tags=['Roles Permissions']
)

@role_permissions_router.post(path='/assing-permission-to-role', response_model=dict, status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer())])
def assing_permission_to_role(role_permission: RolesPermissionsSchema):
    
    db = SessionLocal()
    
    exist_permission = PermissionService(db=db).get_permission(id=role_permission.permission_id)

    if not exist_permission:
        return JSONResponse(content={'message': 'No existe el permiso a asignarle el rol'}, status_code=status.HTTP_404_NOT_FOUND)

    exist_role = RoleService(db=db).get_role(id=role_permission.role_id)

    if not exist_role:
        return JSONResponse(content={'message': 'No existe el rol para asignarle al permiso'}, status_code=status.HTTP_404_NOT_FOUND)
    
    exist_new_role_permission = RolePermissionsService(db=db).get_exist_role_permission(permission_id=role_permission.permission_id, role_id=role_permission.role_id)

    if exist_new_role_permission:
        return JSONResponse(content={'message': 'El permiso ya está asignado'}, status_code=status.HTTP_202_ACCEPTED)

    new_role_permission = RolePermissionsService(db=db).assing_permission_to_role(role_permission=role_permission)

    return JSONResponse(content=jsonable_encoder(new_role_permission), status_code=status.HTTP_201_CREATED)

@role_permissions_router.put(path='/reassing-permission-to-rol/{id}', response_model=dict, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def update_permission(id:  int, role_permission: RolesPermissionsSchema) -> dict:
    
    db = SessionLocal()
    registro = RolePermissionsService(db=db).get_role_permission(id=id)

    if not registro:
        return JSONResponse(content={"message": "Registro no encontrado"}, status_code=status.HTTP_404_NOT_FOUND)

    exist_permission = PermissionService(db=db).get_permission(id=role_permission.permission_id)

    if not exist_permission:
        return JSONResponse(content={'message': 'No existe el permiso a asignarle el rol'}, status_code=status.HTTP_404_NOT_FOUND)

    exist_role = RoleService(db=db).get_role(id=role_permission.role_id)

    if not exist_role:
        return JSONResponse(content={'message': 'No existe el rol para asignarle al permiso'}, status_code=status.HTTP_404_NOT_FOUND)
    
    exist_new_role_permission = RolePermissionsService(db=db).get_exist_role_permission(permission_id=role_permission.permission_id, role_id=role_permission.role_id)

    if exist_new_role_permission:
        return JSONResponse(content={'message': 'El permiso ya está asignado'}, status_code=status.HTTP_202_ACCEPTED)

    registro_editado = RolePermissionsService(db).update_role_permission(id=id, data=role_permission)

    if not registro_editado:
        return JSONResponse(content={"message": "Error al editar"}, status_code=status.HTTP_400_BAD_REQUEST)

    return JSONResponse(content={"message": "Editado", "registro": jsonable_encoder(registro_editado)}, status_code=status.HTTP_200_OK)

@role_permissions_router.delete(path='/delete-permission-role/{id}', response_model=dict, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def delete_permission(id: int) -> dict:

    db = SessionLocal()
    registro = RolePermissionsService(db=db).get_role_permission(id=id)

    if not registro:
        return JSONResponse(content={"message": "Registro No encontrado"}, status_code=status.HTTP_404_NOT_FOUND)

    registro_eliminado = RolePermissionsService(db=db).delete_role_permission(id=id)
    
    if not registro_eliminado:
        return JSONResponse(content={"message": "Error al eliminar"}, status_code=status.HTTP_400_BAD_REQUEST)
    
    return JSONResponse(content={"message": "Eliminado", "registro": jsonable_encoder(registro)}, status_code=status.HTTP_200_OK)

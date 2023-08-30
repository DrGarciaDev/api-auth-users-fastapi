from fastapi import APIRouter, status, Path, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

# modulos locales 
from config.database import SessionLocal
from schemas.permission_schema import PermissionSchemaRequest, PermissionSchemaResponse
from services.permission_service import PermissionService
from middlewares.jwt_bearer import JWTBearer


permission_router = APIRouter(
    prefix='/permissions',
    tags=['Permissions']
)

@permission_router.get(path='/get-all-permissions', response_model=List[PermissionSchemaResponse], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_all_permissions():
    db = SessionLocal()
    registros = PermissionService(db=db).get_permissions()

    return JSONResponse(content=jsonable_encoder(registros), status_code=status.HTTP_200_OK)


@permission_router.get(path='/get-permission/{id}', response_model=PermissionSchemaResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_permission(id: int = Path(ge=1, le=2000)):
    db = SessionLocal()
    registro = PermissionService(db).get_permission(id=id)

    if not registro:
        return JSONResponse(content={"message": "Permiso no encontrado"}, status_code=status.HTTP_404_NOT_FOUND)
        
    return JSONResponse(content=jsonable_encoder(registro), status_code=status.HTTP_200_OK)


@permission_router.post(path='/create-permission', response_model=PermissionSchemaResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer())])
def create_permission(permission: PermissionSchemaRequest):

    db = SessionLocal()
    new_permission = PermissionService(db).create_permission(permission=permission)

    return JSONResponse(content=jsonable_encoder(new_permission), status_code=status.HTTP_201_CREATED)


@permission_router.put(path='/update-permission/{id}', response_model=dict, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def update_permission(id:  int, permission: PermissionSchemaRequest):
    db = SessionLocal()
    registro = PermissionService(db=db).get_permission(id=id)

    if not registro:
        return JSONResponse(content={"message": "Registro no encontrado"}, status_code=status.HTTP_404_NOT_FOUND)

    registro_editado = PermissionService(db).update_permission(id=id, data=permission)

    if not registro_editado:
        return JSONResponse(content={"message": "Error al editar"}, status_code=status.HTTP_400_BAD_REQUEST)

    return JSONResponse(content={"message": "Editado", "registro": jsonable_encoder(registro_editado)}, status_code=status.HTTP_200_OK)


@permission_router.delete(path='/delete-permission/{id}', response_model=dict, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def delete_permission(id: int) -> dict:
    db = SessionLocal()
    registro = PermissionService(db=db).get_permission(id=id)

    if not registro:
        return JSONResponse(content={"message": "Registro No encontrado"}, status_code=status.HTTP_404_NOT_FOUND)

    registro_eliminado = PermissionService(db=db).delete_permission(id=id)
    
    if not registro_eliminado:
        return JSONResponse(content={"message": "Error al eliminar"}, status_code=status.HTTP_400_BAD_REQUEST)
    
    return JSONResponse(content={"message": "Eliminado", "registro": jsonable_encoder(registro)}, status_code=status.HTTP_200_OK)

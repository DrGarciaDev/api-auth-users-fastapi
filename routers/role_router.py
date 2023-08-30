from fastapi import APIRouter, status, Path, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

# modulos locales 
from config.database import SessionLocal
from schemas.role_schema import RoleSchemaRequest, RoleSechemaResponse
from services.role_service import RoleService
from middlewares.jwt_bearer import JWTBearer


role_router = APIRouter(
    prefix='/roles',
    tags=['Roles']
)

@role_router.get(path='/get-all-roles', response_model=List[RoleSechemaResponse], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_all_roles():
    db = SessionLocal()
    registros = RoleService(db=db).get_roles()

    return JSONResponse(content=jsonable_encoder(registros), status_code=status.HTTP_200_OK)


@role_router.get(path='/get-role/{id}', response_model=RoleSechemaResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_role(id: int = Path(ge=1, le=2000)):
    db = SessionLocal()
    registro = RoleService(db).get_role(id=id)

    if not registro:
        return JSONResponse(content={"message": "Rol no encontrado"}, status_code=status.HTTP_404_NOT_FOUND)
        
    return JSONResponse(content=jsonable_encoder(registro), status_code=status.HTTP_200_OK)


@role_router.post(path='/create-role', response_model=RoleSechemaResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer())])
def create_role(role: RoleSchemaRequest):

    db = SessionLocal()
    new_role = RoleService(db).create_role(role=role)

    return JSONResponse(content=jsonable_encoder(new_role), status_code=status.HTTP_201_CREATED)


@role_router.put(path='/update-role/{id}', response_model=dict, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def update_role(id:  int, role: RoleSchemaRequest):
    db = SessionLocal()
    registro = RoleService(db=db).get_role(id=id)

    if not registro:
        return JSONResponse(content={"message": "Registro no encontrado"}, status_code=status.HTTP_404_NOT_FOUND)

    registro_editado = RoleService(db).update_role(id=id, data=role)

    if not registro_editado:
        return JSONResponse(content={"message": "Error al editar"}, status_code=status.HTTP_400_BAD_REQUEST)

    return JSONResponse(content={"message": "Editado", "registro": jsonable_encoder(registro_editado)}, status_code=status.HTTP_200_OK)


@role_router.delete(path='/delete-role/{id}', response_model=dict, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def delete_role(id: int) -> dict:
    db = SessionLocal()
    registro = RoleService(db=db).get_role(id=id)

    if not registro:
        return JSONResponse(content={"message": "Registro No encontrado"}, status_code=status.HTTP_404_NOT_FOUND)

    registro_eliminado = RoleService(db=db).delete_role(id=id)
    
    if not registro_eliminado:
        return JSONResponse(content={"message": "Error al eliminar"}, status_code=status.HTTP_400_BAD_REQUEST)
    
    return JSONResponse(content={"message": "Eliminado", "registro": jsonable_encoder(registro)}, status_code=status.HTTP_200_OK)

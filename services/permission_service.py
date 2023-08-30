from models.permission_model import PermissionModel
from schemas.permission_schema import PermissionSchemaRequest
from datetime import datetime


class PermissionService():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_permissions(self):
        registros = self.db.query(PermissionModel).all()
        return registros
    
    def get_permission(self, id):
        registro = self.db.query(PermissionModel).filter(PermissionModel.id == id).first()
        return registro
    
    def create_permission(self, permission: PermissionSchemaRequest):
        new_permission = PermissionModel(**permission.dict())

        self.db.add(new_permission)
        self.db.commit()
        self.db.refresh(new_permission)

        return new_permission
    
    def update_permission(self, id: int, data: PermissionSchemaRequest):
        registro = self.db.query(PermissionModel).filter(PermissionModel.id == id).first()

        registro.name = data.name
        registro.description = data.description
        registro.updated_at = datetime.now()

        self.db.commit()
        self.db.refresh(registro)

        return registro
    
    
    def delete_permission(self, id: int):
        registro = self.db.query(PermissionModel).filter(PermissionModel.id == id).delete()
        self.db.commit()

        return registro
from models.role_permissions_model import RolePermissionsModel
from schemas.role_permissions_schema import RolesPermissionsSchema
from datetime import datetime

class RolePermissionsService():
    def __init__(self, db) -> None:
        self.db = db

    def get_role_permission(self, id):
        registro = self.db.query(RolePermissionsModel).filter(RolePermissionsModel.id == id).first()
        return registro
    
    def get_exist_role_permission(self, role_id, permission_id):
        registro = self.db.query(RolePermissionsModel).filter(RolePermissionsModel.role_id == role_id).filter(RolePermissionsModel.permission_id == permission_id).first()
        return registro
    
    def assing_permission_to_role(self, role_permission: RolesPermissionsSchema):
        new_role_permission = RolePermissionsModel(**role_permission.dict())

        self.db.add(new_role_permission)
        self.db.commit()
        self.db.refresh(new_role_permission)

        return new_role_permission
    
    def update_role_permission(self, id: int, data: RolesPermissionsSchema):
        registro = self.db.query(RolePermissionsModel).filter(RolePermissionsModel.id == id).first()

        registro.role_id = data.role_id
        registro.permission_id = data.permission_id
        registro.updated_at = datetime.now()

        self.db.commit()
        self.db.refresh(registro)

        return registro
    
    def delete_role_permission(self, id: int):
        registro = self.db.query(RolePermissionsModel).filter(RolePermissionsModel.id == id).delete()
        self.db.commit()

        return registro
from models.role_model import RoleModel
from schemas.role_schema import RoleSchemaRequest
from datetime import datetime


class RoleService():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_roles(self):
        registros = self.db.query(RoleModel).all()
        return registros
    
    def get_role(self, id):
        registro = self.db.query(RoleModel).filter(RoleModel.id == id).first()
        return registro
    
    def create_role(self, role: RoleSchemaRequest):
        new_role = RoleModel(**role.dict())

        self.db.add(new_role)
        self.db.commit()
        self.db.refresh(new_role)

        return new_role
    
    def update_role(self, id: int, data: RoleSchemaRequest):
        registro = self.db.query(RoleModel).filter(RoleModel.id == id).first()

        registro.name = data.name
        registro.description = data.description
        registro.updated_at = datetime.now()

        self.db.commit()
        self.db.refresh(registro)

        return registro
    
    
    def delete_role(self, id: int):
        registro = self.db.query(RoleModel).filter(RoleModel.id == id).delete()
        self.db.commit()

        return registro
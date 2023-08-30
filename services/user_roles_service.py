from models.user_roles_model import UserRolesModel
from schemas.user_roles_schema import UserRolesSchema
from datetime import datetime

class UserRolesService():
    def __init__(self, db) -> None:
        self.db = db

    def get_user_role(self, id):
        registro = self.db.query(UserRolesModel).filter(UserRolesModel.id == id).first()
        return registro
    
    def get_exist_user_role(self, user_id, role_id):
        registro = self.db.query(UserRolesModel).filter(UserRolesModel.user_id == user_id).filter(UserRolesModel.role_id == role_id).first()
        return registro
    
    def assing_role_to_user(self, user_role: UserRolesSchema):
        new_user_role = UserRolesModel(**user_role.dict())

        self.db.add(new_user_role)
        self.db.commit()
        self.db.refresh(new_user_role)

        return new_user_role
    
    def update_user_role(self, id: int, data: UserRolesSchema):
        registro = self.db.query(UserRolesModel).filter(UserRolesModel.id == id).first()

        registro.user_id = data.user_id
        registro.role_id = data.role_id
        registro.updated_at = datetime.now()

        self.db.commit()
        self.db.refresh(registro)

        return registro
    
    def delete_user_role(self, id: int):
        registro = self.db.query(UserRolesModel).filter(UserRolesModel.id == id).delete()
        self.db.commit()

        return registro
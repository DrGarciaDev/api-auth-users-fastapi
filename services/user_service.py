from datetime import datetime

from models.user_model import UserModel
from models.user_roles_model import UserRolesModel
from models.role_model import RoleModel
from models.role_permissions_model import RolePermissionsModel
from models. permission_model import PermissionModel

from schemas.user_schema import UserSchema

class UserService():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_users(self):
        registros = self.db.query(UserModel).all()
        return registros
    
    def get_user(self, id):
        registro = self.db.query(UserModel).filter(UserModel.id == id).first()

        return registro
    
    def create_user(self, user: UserSchema):
        new_user = UserModel(**user.dict())

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user
    
    def update_user(self, id: int, data: UserSchema):
        registro = self.db.query(UserModel).filter(UserModel.id == id).first()

        registro.name = data.name
        registro.email = data.email
        registro.password = data.password
        registro.status = data.status
        registro.updated_at = datetime.now()

        self.db.commit()

        return registro
    
    def delete_user(self, id: int):
        registro = self.db.query(UserModel).filter(UserModel.id == id).delete()
        self.db.commit()

        return registro
    
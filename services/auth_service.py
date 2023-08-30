from datetime import datetime

from models.user_model import UserModel
from models.user_roles_model import UserRolesModel
from models.role_model import RoleModel
from models.role_permissions_model import RolePermissionsModel
from models. permission_model import PermissionModel

from schemas.auth_schema import AuthRegisterUserRequestSchema


class AuthService():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_user_by_email(self, email):
        usuario = self.db.query(UserModel).filter(UserModel.email == email).first()

        roles = self.db.query(RoleModel)\
                                .join(UserRolesModel, UserRolesModel.role_id == RoleModel.id)\
                                .join(UserModel, UserModel.id == UserRolesModel.user_id)\
                                .filter(UserRolesModel.user_id == usuario.id)\
                                .all()
        
        list_permissions = []

        for rol in roles:
            permissions = self.db.query(PermissionModel)\
                                    .join(RolePermissionsModel, RolePermissionsModel.permission_id == PermissionModel.id)\
                                    .join(RoleModel, RoleModel.id == RolePermissionsModel.role_id)\
                                    .filter(RolePermissionsModel.role_id == rol.id)\
                                    .all()
            
            for permission in permissions:
                list_permissions.append(permission)
        
        registro = {
            'user': usuario,
            'roles': roles,
            'permissions': list_permissions
        }

        return registro
    
    def register_user(self, user: AuthRegisterUserRequestSchema):
        new_user = UserModel(**user.dict())

        self.db.add(new_user)
        self.db.commit()

        registro = self.db.query(UserModel).filter(UserModel.id == new_user.id).first()

        return registro
    
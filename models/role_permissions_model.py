from config.database import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class RolePermissionsModel(Base):
    __tablename__ = 'role_permissions'

    id            = Column(Integer, primary_key=True, autoincrement=True)

    permission_id = Column(Integer, ForeignKey('permissions.id', ondelete='RESTRICT'))
    role_id       = Column(Integer, ForeignKey('roles.id', ondelete='RESTRICT'))
    created_at    = Column(DateTime, default=datetime.now)
    updated_at    = Column(DateTime, default=None)

    role          = relationship('RoleModel', back_populates='role_permissions')
    permission    = relationship('PermissionModel', back_populates='permission_roles')
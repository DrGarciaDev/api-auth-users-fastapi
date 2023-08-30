from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class RoleModel(Base):
    __tablename__    = 'roles'

    id               = Column(Integer, primary_key=True, autoincrement=True)
    name             = Column(String)
    description      = Column(String)
    created_at       = Column(DateTime, default=datetime.now)
    updated_at       = Column(DateTime, default=None)


    role_users       = relationship('UserRolesModel', back_populates='role')
    role_permissions = relationship('RolePermissionsModel', back_populates='role')
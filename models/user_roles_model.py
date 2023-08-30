from config.database import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class UserRolesModel(Base):
    __tablename__ = 'user_roles'

    id            = Column(Integer, primary_key=True, autoincrement=True)

    user_id       = Column(Integer, ForeignKey('users.id', ondelete='RESTRICT'))
    role_id       = Column(Integer, ForeignKey('roles.id', ondelete='RESTRICT'))
    created_at    = Column(DateTime, default=datetime.now)
    updated_at    = Column(DateTime, default=None)

    user          = relationship('UserModel', back_populates='user_roles')
    role          = relationship('RoleModel', back_populates='role_users')
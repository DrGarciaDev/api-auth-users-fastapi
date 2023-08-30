from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class PermissionModel(Base):
    __tablename__    = 'permissions'

    id               = Column(Integer, primary_key=True, autoincrement=True)
    name             = Column(String)
    description      = Column(String)
    created_at       = Column(DateTime, default=datetime.now)
    updated_at       = Column(DateTime, default=None)

    permission_roles = relationship('RolePermissionsModel', back_populates='permission')
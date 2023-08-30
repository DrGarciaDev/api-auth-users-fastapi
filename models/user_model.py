from config.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

class UserModel(Base):
    __tablename__ = 'users'

    id            = Column(Integer, primary_key=True, autoincrement=True)
    name          = Column(String)
    email         = Column(String)
    password      = Column(Text)
    status        = Column(Boolean)
    created_at    = Column(DateTime, default=datetime.now)
    updated_at    = Column(DateTime, default=None)
    
    user_roles    = relationship('UserRolesModel', back_populates='user')
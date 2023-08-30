from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class UserSchema(BaseModel):
    name: str                      = Field(example='Luis Alberto García Rodríguez', min_length=20, max_length=100)
    email: EmailStr                = Field(example='admin@gmail.com')
    password: str                  = Field(example='123456', min_length=6, max_length=60)
    status: bool                   = Field(example=True)
    created_at: datetime           = Field(example=datetime.now())
    updated_at: Optional[datetime] = Field(example=None)

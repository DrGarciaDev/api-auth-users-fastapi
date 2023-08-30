from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class AuthLoginUserRequestSchema(BaseModel):
    email: EmailStr = Field(example="admin@gmail.com")
    password: str   = Field(example='123456', min_length=6, max_length=50)

class AuthRegisterUserRequestSchema(AuthLoginUserRequestSchema):
    name: str    = Field(example='Luis Alberto García Rodríguez', min_length=10, max_length=100)
    status: bool = Field(example=True)
    
class AuthRegisterUserResponseSchema(BaseModel):
    id: int                        = Field(example=1)
    email: EmailStr                = Field(example="admin@gmail.com")
    name: str                      = Field(example='Luis Alberto García Rodríguez', min_length=10, max_length=100)
    status: bool                   = Field(example=True)
    created_at: datetime           = Field(example=datetime.now())
    updated_at: Optional[datetime] = Field(example=None)


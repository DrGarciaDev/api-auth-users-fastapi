from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserRolesSchema(BaseModel):
    user_id: int = Field(example=1, ge=1, lt=100)
    role_id: int = Field(example=1, ge=1, lt=100)
   
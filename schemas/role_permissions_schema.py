from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RolesPermissionsSchema(BaseModel):
    role_id: int       = Field(example=1, ge=1, lt=100)
    permission_id: int = Field(example=1, ge=1, lt=100)

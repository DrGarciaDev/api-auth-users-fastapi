from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RoleSchemaRequest(BaseModel):
    name: str                      = Field(example='Super admin', min_length=2, max_length=100)
    description: str               = Field(example='Permiso sobre todo el sistema', min_length=10, max_length=100)
    
class RoleSechemaResponse(BaseModel):
    id: int                        = Field(example=1)
    name: str                      = Field(example='Super admin', min_length=2, max_length=100)
    description: str               = Field(example='Permiso sobre todo el sistema', min_length=10, max_length=100)
    created_at: datetime           = Field(example=datetime.now())
    updated_at: Optional[datetime] = Field(example=None)
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PermissionSchemaRequest(BaseModel):
    name: str                      = Field(example='Ver usuarios', min_length=5, max_length=100)
    description: str               = Field(example='Permiso para ver usuarios', min_length=5, max_length=100)
    
class PermissionSchemaResponse(BaseModel):
    id: int                        = Field(example=1)
    name: str                      = Field(example='Ver usuarios', min_length=5, max_length=100)
    description: str               = Field(example='Permiso para ver usuarios', min_length=5, max_length=100)
    created_at: datetime           = Field(example=datetime.now())
    updated_at: Optional[datetime] = Field(example=None)
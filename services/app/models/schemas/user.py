from typing import Optional
from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    name: str = Field(..., max_length=100)
    user_id : Optional[str]
    email: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Surendar",
                "email": "user@example.com"
            }
        }
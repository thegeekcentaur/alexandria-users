from typing import List, Optional
from pydantic import BaseModel, Field

class CatalogSchema(BaseModel):
    name: str = Field(..., min_length=2)
    user_id :str
    description: Optional[str]
    books_list: Optional[List[str]]

    class Config:
        schema_extra = {
            "example": {
                "name": "Favourites",
                "user_id": "Bob",
                "description": "To Read",
                "books_list": [
                    "9780684846842",
                    "9780684846845"
                ]
            }
        }

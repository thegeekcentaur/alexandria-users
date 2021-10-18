from typing import List
from pydantic import BaseModel

class CatalogBookSchema(BaseModel):
    books_list: List[str]
    class Config:
        schema_extra = {
            "example": {
                "books_list": [
                    "9780684846842",
                    "9780684846845"
                ]
            }
        }

from pydantic import BaseModel
from typing import Optional

class ShelfCreate(BaseModel):
    shelf_code:str
    floor:int



class Bookcreate(BaseModel):
    isbn:str
    title:str
    author:str
    publisher:str
    category:str
    shelf_id:int
    quantity:int
    image_url: Optional[str]=None

    
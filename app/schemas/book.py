from pydantic import BaseModel

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

    
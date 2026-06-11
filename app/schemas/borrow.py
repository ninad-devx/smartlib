from pydantic import BaseModel

class Borrowcreate(BaseModel):

    university_id: str
    book_id: int
    borrow_days: int


class Returnbook(BaseModel):
    borrow_id:int

    
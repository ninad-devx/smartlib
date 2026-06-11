from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base

class Book(Base):
    __tablename__="books"


    id=Column(Integer, primary_key=True)

    isbn=Column(String(30),unique=True)

    title=Column(String(255),nullable=False)

    author=Column(String(255))

    publisher=Column(String(255))

    category=Column(String(100))

    shelf_id=Column(Integer,ForeignKey("shelves.id"))

    quantity=Column(Integer,default=0)

    available_quantity=Column(Integer,default=0)

    shelf = relationship("Shelf")

    
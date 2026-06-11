from sqlalchemy import Column,Integer,DateTime,ForeignKey,Enum
from sqlalchemy.orm import relationship
from app.core.database import Base

class Borrowrecord(Base):
    __tablename__="borrow_records"

    id=Column(Integer,primary_key=True)

    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)

    book_id=Column(Integer,ForeignKey("books.id"),nullable=False)

    borrow_date=Column(DateTime,nullable=False)

    due_date=Column(DateTime,nullable=True)

    status=Column(DateTime,nullable=True)

    status=Column(Enum(
        "borrowed",
        "returned", 
        "overdue"
    ),
    default="borrowed" 
    )
    user = relationship(
    "User"
   )

    book = relationship(
     "Book"
    )
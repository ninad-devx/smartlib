from sqlalchemy import Column,Integer,String,Boolean,DateTime,Enum
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)

    university_id=Column(String(50),unique=True,nullable=False)

    name=Column(String(100),nullable=False)

    email=Column(String(120),unique=True,nullable=False)

    password_hash=Column(String(255),nullable=False)

    role=Column(Enum(
        "student",
        "teacher",
        "librarian",
        name="user_role_enum"
    ),nullable=False)

    department=Column(String(100))

    rfid_uid=Column(String(50),unique=True,nullable=True)

    is_active=Column(Boolean,default=True)

    created_at=Column(DateTime,default=datetime.utcnow)

    borrow_records=relationship("Borrowrecord")
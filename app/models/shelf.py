from sqlalchemy import Column,Integer,String
from app.core.database import Base

class Shelf(Base):

    __tablename__="shelves"

    id=Column(Integer,primary_key=True,index=True)

    shelf_code=Column(String(20),unique=True,nullable=False)

    floor=Column(Integer,nullable=False)
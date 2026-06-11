from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

USER=os.getenv("USER")
PASSWORD=os.getenv("PASSWORD")
HOST=os.getenv("HOST")
PORT=os.getenv("PORT")
DATABASE=os.getenv("DATABASE")

DATABASE_URL=(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

engine=create_engine(DATABASE_URL,echo=True)

Sessionlocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)


Base=declarative_base()

def get_db():
   db = Sessionlocal()
   try:
       yield db
   finally:
       db.close()
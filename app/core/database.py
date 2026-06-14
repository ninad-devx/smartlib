from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import urllib.parse

load_dotenv()

USER=os.getenv("USER")
PASSWORD=os.getenv("PASSWORD")
HOST=os.getenv("HOST")
PORT=os.getenv("PORT")
DATABASE=os.getenv("DATABASE")

# 2. Safely encode the password to protect the '&' character
SAFE_PASSWORD = urllib.parse.quote_plus(PASSWORD) if PASSWORD else ""

# Updated: Removed &supavisor_session=true to keep psycopg2 happy
DATABASE_URL = (
    f"postgresql+psycopg2://{USER}:{SAFE_PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    "?sslmode=require"
)

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

Sessionlocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)


Base=declarative_base()

def get_db():
   db = Sessionlocal()
   try:
       yield db
   finally:
       db.close()
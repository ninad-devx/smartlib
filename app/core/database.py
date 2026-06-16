from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import urllib.parse

load_dotenv()

DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_DATABASE=os.getenv("DB_DATABASE")

# 2. Safely encode the password to protect the '&' character
SAFE_PASSWORD = urllib.parse.quote_plus(DB_PASSWORD) if DB_PASSWORD else ""

# Updated: Removed &supavisor_session=true to keep psycopg2 happy
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{SAFE_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
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
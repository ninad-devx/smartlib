from app.core.database import Base
from app.core.database import engine

# Import ALL models

from app.models.user import User
from app.models.shelf import Shelf
from app.models.book import Book
from app.models.attendance import Attendancelog
from app.models.borrow import Borrowrecord
from app.models.renewal import RenewalRequest
from app.models.fine import Fine
from app.models.audit import AuditLog

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")
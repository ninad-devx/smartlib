from sqlalchemy import Column,Integer,DateTime,ForeignKey

from app.core.database import Base

class Attendancelog(Base):
    __tablename__="attendance_logs"

    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)

    entry_time=Column(DateTime,nullable=False)

    exit_time=Column(DateTime,nullable=True)

    duration_minutes=Column(Integer,nullable=True)
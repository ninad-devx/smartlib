from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DECIMAL
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey

from app.core.database import Base


class Fine(Base):

    __tablename__ = "fines"

    id = Column(Integer, primary_key=True)

    borrow_id = Column(
        Integer,
        ForeignKey("borrow_records.id"),
        nullable=False
    )

    amount = Column(
        DECIMAL(10, 2),
        default=0
    )

    paid = Column(
        Boolean,
        default=False
    )
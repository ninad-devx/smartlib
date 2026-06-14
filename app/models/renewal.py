from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Enum

from app.core.database import Base


class RenewalRequest(Base):

    __tablename__ = "renewal_requests"

    id = Column(Integer, primary_key=True)

    borrow_id = Column(
        Integer,
        ForeignKey("borrow_records.id"),
        nullable=False
    )

    request_date = Column(
        DateTime,
        nullable=False
    )

    status = Column(
        Enum(
            "pending",
            "approved",
            "rejected",
            name="renewal_status_enum"

        ),
        default="pending"
    )
    requested_days = Column(Integer)
    
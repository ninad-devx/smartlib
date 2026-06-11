from pydantic import BaseModel

class RenewalRequestCreate(
    BaseModel
):
    borrow_id: int
    requested_days: int


class RenewalApprove(
    BaseModel
):
    renewal_id: int
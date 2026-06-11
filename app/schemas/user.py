from pydantic import BaseModel
from pydantic import EmailStr

class RegisterSchema(BaseModel):
    university_id: str
    name: str
    email: EmailStr
    password: str
    department: str
    role: str


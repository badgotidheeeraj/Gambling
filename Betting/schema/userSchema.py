from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    id:int
    first_name: str
    last_name: str
    password: str
    phone: str
    address: str
    pic: str
    dob: str
    email: EmailStr
    age: int | None = None




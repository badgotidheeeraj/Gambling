from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserCreate(BaseModel):
    id: int
    first_name: str
    last_name: str
    password: str
    phone: str
    address: str
    pic: str
    dob: date  
    email: EmailStr
    age: Optional[int] = None



dic = {
    "id": 1,
    "first_name": "dheeraj",
    "last_name": "heeraj",
    "password": "1321654",
    "phone": "7500003264",
    "address": "dshflskjhfl",
    "pic": "dshflskjhfl",
    "dob": "2000-05-26",  # Valid date
    "email": "badgoti@gmal.com",
    "age": 15
}



print(UserCreate(**dic))
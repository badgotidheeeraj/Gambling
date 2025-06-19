from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, Optional
from datetime import date, datetime

class UserCreate(BaseModel):
    id: Annotated[int, Field(title="User ID", example=1)]
    username: Annotated[str,Field(title="username ", example="joyfull")]
    email: Annotated[EmailStr, Field(title="Email Address", example="user@example.com")]
    password: Annotated[str, Field(max_length=50, title="Password", example="SecurePass123!")]
    balance: Annotated[float, Field(title="User Balance", example=100.0)]
    phone: Annotated[str, Field(title="Phone Number", example="1234567890")]
    pic: Annotated[date, Field(title="Profile Date (DOB, etc.)", example="1990-01-01")]
    created_at: Annotated[datetime, Field(title="Created At", example="2025-06-19T12:34:56")]
    is_active: Annotated[Optional[bool], Field(title="Is Active", example=True, default=True)]
    
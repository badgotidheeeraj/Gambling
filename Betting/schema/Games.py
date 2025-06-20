
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, Optional
from datetime import date, datetime



class cashSchema(BaseModel): 
    cash:str
    gamePoint:str
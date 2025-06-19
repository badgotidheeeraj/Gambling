
from sqlalchemy import Column, Integer, String, Date
from configdb.connection import Base,engine


class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)  # autoincrement=True is default
    username=Column(String, primary_key=True, index=True)
    email = Column(String, index=True)
    password = Column(String, index=True)
    balance = Column(Integer, index=True)
    phone = Column(String, index=True)
    pic = Column(String, index=True) 
    created_at = Column(Date, index=True)  # Changed from String to Date and removed unique=True
    is_active = Column(String, index=True)

Base.metadata.create_all(bind=engine)





    
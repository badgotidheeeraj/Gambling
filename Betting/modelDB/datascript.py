
from sqlalchemy import Column, Integer, String, Date
from configdb.connection import Base,engine


class UserProfile(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # autoincrement=True is default
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    password = Column(String, index=True)
    age = Column(Integer, index=True)
    email = Column(String, index=True)
    phone = Column(String, index=True)
    address = Column(String, index=True)
    pic = Column(String, index=True) 
    dob = Column(Date, index=True)  # Changed from String to Date and removed unique=True

Base.metadata.create_all(bind=engine)

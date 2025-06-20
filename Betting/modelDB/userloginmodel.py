from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from configdb.connection import engine
import uuid
from sqlalchemy.orm import relationship

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    balance = Column(Integer, nullable=True)
    phone = Column(String, nullable=False)
    pic = Column(Date, nullable=True)
    created_at = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)    
    otp = relationship("Otp", back_populates="user", uselist=False)

Base.metadata.create_all(bind=engine)

    
    
    
    
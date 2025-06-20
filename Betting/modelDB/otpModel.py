from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
import uuid

from modelDB.userloginmodel import Users, Base  
from configdb.connection import engine

class Otp(Base):
    __tablename__ = "otp"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    otp = Column(String, nullable=True)
    otp_created_at = Column(DateTime, nullable=True)
    is_verified = Column(Boolean, default=False)

    user = relationship("Users", back_populates="otp")

    
Base.metadata.create_all(bind=engine)

    
    
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

class GameRound(Base):
    __tablename__ = 'game_rounds'    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    crash_multiplier = Column(Float, nullable=False) 
        
    bets = relationship("Bet", back_populates="round")
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()
class Bet(Base):
    __tablename__ = 'bets'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    round_id = Column(String(36), ForeignKey('game_rounds.id'), nullable=False)    
    bet_amount = Column(Float, nullable=False)
    cashout_multiplier = Column(Float, nullable=True)  # Null = didn’t cash out in time
    won_amount = Column(Float, default=0.0)
    is_winner = Column(Boolean, default=False)    
    user = relationship("User", back_populates="bets")
    round = relationship("GameRound", back_populates="bets")
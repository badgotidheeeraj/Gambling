import uuid
from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime

Base = declarative_base()

class GameType(enum.Enum):
    roulette = "roulette"
    slots = "slots"
    blackjack = "blackjack"
    sports = "sports"
    custom = "custom"

class GameStatus(enum.Enum):
    active = "active"
    inactive = "inactive"

class Games(Base):
    __tablename__ = "games"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    game_type = Column(Enum(GameType), nullable=False)
    status = Column(Enum(GameStatus), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

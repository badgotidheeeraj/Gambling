import uuid
from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class RoundStatus(enum.Enum):
    open = "open"
    closed = "closed"
    settled = "settled"

class GameRounds(Base):
    __tablename__ = "game_rounds"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    game_id = Column(UUID(as_uuid=True), ForeignKey("games.id"), nullable=False)
    round_number = Column(Integer, nullable=False)
    status = Column(Enum(RoundStatus), nullable=False)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)

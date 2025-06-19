import uuid
from sqlalchemy import Column, String, DECIMAL, ForeignKey, DateTime, Enum, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BetResultEnum(str, Enum):
    win = "win"
    lose = "lose"
    pending = "pending"

class Bet(Base):
    __tablename__ = "bets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    game_id = Column(UUID(as_uuid=True), ForeignKey("games.id"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    odds = Column(DECIMAL(5, 2), nullable=True)
    potential_win = Column(DECIMAL(10, 2), nullable=True)
    result = Column(
        Enum(BetResultEnum),
        nullable=False,
        default=BetResultEnum.pending,
        server_default="pending"
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint("result IN ('win', 'lose', 'pending')", name="check_result_valid"),
    )

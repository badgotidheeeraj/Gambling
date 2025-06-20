from sqlalchemy import (Column, String, Text, DECIMAL, Enum, ForeignKey, TIMESTAMP, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import enum
import uuid

# Enum for transaction types
class TransactionType(str, enum.Enum):
    deposit = 'deposit'
    withdrawal = 'withdrawal'
    bet = 'bet'
    win = 'win'
    refund = 'refund'

# Base class for all models
class Base(DeclarativeBase):
    pass

# WalletTransactions model
class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType, name="transaction_type"), nullable=False)
    amount: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    balance_after: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    # Optional: Relationship to User model
    user = relationship("User", back_populates="wallet_transactions")

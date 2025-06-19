import uuid
from sqlalchemy import Column, String, Text, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

Base = declarative_base()

class AdminRoleEnum(str, Enum):
    admin = "admin"
    operator = "operator"
    analyst = "analyst"

class Admin(Base):
    __tablename__ = "admins"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(
        String,
        nullable=False,
        default=AdminRoleEnum.admin.value,
        server_default=AdminRoleEnum.admin.value
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "role IN ('admin', 'operator', 'analyst')",
            name="check_admin_role_valid"
        ),
    )

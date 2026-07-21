import enum
from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from datetime import datetime, timezone
from app.database.base import Base


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text)
    email = Column(String, index=True)
    phone_number = Column(String)
    hashed_password = Column(String)
    role = Column(PG_ENUM(UserRole, name="userrole", create_type=False, values_callable=lambda obj: [e.value for e in obj]), default=UserRole.USER, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))





from sqlalchemy import Column, String, Integer, DateTime, Text
from datetime import datetime, timezone
from app.database.base import Base

class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text)
    email = Column(String, index=True)
    phone_number = Column(String)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))





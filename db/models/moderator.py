from sqlalchemy import Column, Integer, BigInteger, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Moderator(Base):
    __tablename__ = "moderators"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    full_name = Column(Text)
    added_at = Column(DateTime(timezone=True), server_default=func.now())

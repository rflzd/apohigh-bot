from sqlalchemy import Column, Integer, BigInteger, Text, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    full_name = Column(Text)
    is_subscribed = Column(Boolean, default=False)
    favorite_teams = Column(Text)  # JSON, string və ya vergüllə ayrılmış format
    coupon_upload_link = Column(Text)
    payment_proof_url = Column(Text)
    subscription_start = Column(DateTime, nullable=True)
    subscription_end = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

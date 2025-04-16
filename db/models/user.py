from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from db.base import Base  # Make sure to import Base from the correct location

class User(Base):
    __tablename__ = "users"

    # Columns for the User model
    telegram_id = Column(BigInteger, primary_key=True, index=True)  # Telegram ID as the primary key
    full_name = Column(String(255))  # VARCHAR(255)
    is_subscribed = Column(Boolean, default=False)  # Subscription status, default is False
    favorite_teams = Column(JSON)  # JSON format to store user's favorite teams
    coupon_upload_link = Column(String(255))  # Stores the coupon link
    payment_proof_url = Column(String(255))  # Stores the payment proof link
    subscription_start = Column(DateTime, nullable=True)  # Nullable start time for subscription
    subscription_end = Column(DateTime, nullable=True)  # Nullable end time for subscription
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Automatically set when the user is created

    @classmethod
    def get_user(cls, telegram_id):
        """Retrieve user by telegram_id"""
        return cls.query.filter_by(telegram_id=telegram_id).first()


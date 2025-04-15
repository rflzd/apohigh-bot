from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from db.models import Base  # Burada Base modelini import edirik

class User(Base):
    __tablename__ = "users"

    telegram_id = Column(BigInteger, primary_key=True, index=True)
    full_name = Column(String(255))  # VARCHAR(255)
    is_subscribed = Column(Boolean, default=False)
    favorite_teams = Column(JSON)  # JSON formatında saxlanır
    coupon_upload_link = Column(String(255))  # VARCHAR(255)
    payment_proof_url = Column(String(255))  # VARCHAR(255)
    subscription_start = Column(DateTime, nullable=True)
    subscription_end = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    @classmethod
    def get_user(cls, telegram_id):
        return cls.query.filter_by(telegram_id=telegram_id).first()  # Veritabanından istifadəçi məlumatını alır

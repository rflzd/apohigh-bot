from sqlalchemy import Column, Integer, String
from db.db import Base  # db.py-dəki Base istifadə edirik

class FavoriteTeam(Base):
    __tablename__ = 'favorite_teams'  # Cədvəl adı

    id = Column(Integer, primary_key=True, autoincrement=True)
    team_name = Column(String, nullable=False)  # Komandanın adı
    user_id = Column(Integer, nullable=False)  # İstifadəçi ID-si

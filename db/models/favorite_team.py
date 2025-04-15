from sqlalchemy import Column, Integer, String
from db.models import Base  # Burada Base modelini import edirik

class FavoriteTeam(Base):
    __tablename__ = "favorite_teams"

    id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String(255))  # VARCHAR(255)

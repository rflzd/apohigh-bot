from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)  # Komandanın unikal ID-si
    team_name = Column(String(255), nullable=False)     # Komandanın adı
    league_id = Column(Integer, ForeignKey('leagues.id'), nullable=False)  # Liqa ID-si

    league = relationship("League", back_populates="teams")  # Liqa ilə əlaqə

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.base import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, unique=True, nullable=False)
    league_id = Column(Integer, ForeignKey('leagues.id'), nullable=False)  # ForeignKey əlavə edirik
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)

    # Relationship bağlantısını birbaşa modeldə göstəririk
    league = relationship("League", back_populates="matches")  # League ilə əlaqəni bu şəkildə qururuq

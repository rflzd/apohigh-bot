from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.db import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, unique=True, nullable=False)
    league_id = Column(Integer, ForeignKey('leagues.id'), nullable=False)  # ForeignKey əlavə edirik
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)

    # Late import: relationship-i yalnız lazım olduqda import edirik
    @property
    def league(self):
        from db.models.league import League  # Burada League modelini yalnız lazım olduğu zaman import edirik
        return relationship("League", back_populates="matches")

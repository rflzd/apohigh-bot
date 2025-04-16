from sqlalchemy import Column, Integer, String
from db.base import Base
from sqlalchemy.orm import relationship

class League(Base):
    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True, index=True)
    league_name = Column(String, unique=True, nullable=False)

    # League modelində matches ilə əlaqəni göstəririk
    matches = relationship("Match", back_populates="league")

from sqlalchemy import Column, Integer, String
from db.base import Base 
from sqlalchemy.orm import relationship

class League(Base):
    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)

    # Liqanın əlaqəli matçları
    matches = relationship("Match", back_populates="league")

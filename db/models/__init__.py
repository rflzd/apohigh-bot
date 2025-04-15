from sqlalchemy.ext.declarative import declarative_base

# Base modelini burada təyin edirik
Base = declarative_base()

# Modelləri import edirik
from .user import User  # User modelini import edirik
from .favorite_team import FavoriteTeam  # FavoriteTeam modelini import edirik

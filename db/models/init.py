from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy Base modelini təyin edirik
Base = declarative_base()

# İstədiyiniz modelləri import edirsiniz
from .user import User
from .favorite_team import FavoriteTeam

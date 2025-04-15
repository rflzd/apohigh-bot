from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base  # Base modelini import edirik
from config import DATABASE_URL  # DATABASE_URL config faylından alınır

# Engine və session konfiqurasiyası
engine = create_engine(DATABASE_URL)  # connect_args parametresi lazım deyil
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base modelini deklarativ bazaya əlavə edirik
Base = declarative_base()

def init_db():
    # Veritabanı cədvəllərini yaratmaq
    Base.metadata.create_all(bind=engine)
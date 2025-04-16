from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base  # Burada Base modelini import edirik
from config import DATABASE_URL  # DATABASE_URL config faylından alınır

# Engine və session konfiqurasiyası
engine = create_engine(DATABASE_URL)  # connect_args parametresi lazım deyil
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Veritabanı cədvəllərini yaratmaq
    Base.metadata.create_all(bind=engine)
    print('✅ Database cədvəlləri yaradıldı')

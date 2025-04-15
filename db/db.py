from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base  # Bu əslində doğru yerləşdirilmişdir
from config import DATABASE_URL

# Veritabanı engine və session konfiqurasiyası
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # SQLite üçün əlavə etdik (əgər SQLite istifadə olunursa)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy bazası
Base = declarative_base()

# Veritabanı cədvəllərini yaratmaq üçün funksiyanı əlavə edə bilərik
def init_db():
    Base.metadata.create_all(bind=engine)

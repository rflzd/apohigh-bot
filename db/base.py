import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# .env faylındakı dəyişənləri oxumaq üçün
load_dotenv()

# İndi DATABASE_URL artıq mövcuddur
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("❌ DATABASE_URL not found. .env file properly loaded?")

# SQLAlchemy üçün baza obyektləri
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

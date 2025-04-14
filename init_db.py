from db.db import engine
from db.models.user import Base

def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Database cədvəlləri yaradıldı")

if __name__ == "__main__":
    init_db()

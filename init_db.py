from db.db import engine
from db.models import Base  # Düzgün Base modelini import edirik

def init_db():
    # Veritabanı cədvəllərini yaratmaq
    Base.metadata.create_all(bind=engine)
    print('✅ Database cədvəlləri yaradıldı')

if __name__ == '__main__':
    init_db()

from db.base import engine, Base  # Engine və Base import edirik
from db.models import match, league  # Modelləri burada çağırmalıyıq

def init_db():
    Base.metadata.create_all(bind=engine)  # Cədvəlləri yaratmaq
    print('✅ Database cədvəlləri yaradıldı')

if __name__ == '__main__':
    init_db()  # Veritabanı cədvəllərini yaradırıq

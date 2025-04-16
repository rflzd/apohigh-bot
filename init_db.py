from db.base import engine, Base  # ← doğru yer
from db.models import match, league  # modelləri burada çağırmalıyıq

def init_db():
    Base.metadata.create_all(bind=engine)
    print('✅ Database cədvəlləri yaradıldı')

if __name__ == '__main__':
    init_db()

from db.db import engine, Base  # Engine və Base import edirik
from db.models import League, Match, User, FavoriteTeam, Team  # Cədvəlləri import edirik

def init_db():
    Base.metadata.create_all(bind=engine)  # Cədvəlləri yaratmaq
    print('✅ Database cədvəlləri yaradıldı')

if __name__ == '__main__':
    init_db()

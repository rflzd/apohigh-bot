from db.base import Base, engine

def init_db():
    from db.models import match, league  # Modellər bu səviyyədə import olunur
    Base.metadata.create_all(bind=engine)

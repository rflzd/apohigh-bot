# main.py

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routes import index
from app.routes import index, live
from fastapi import FastAPI
from app.utils import fetch_from_highlightly
from app.services.highlightly import save_highlight_matches_to_db
from app.database.database import get_async_session
from dotenv import load_dotenv
load_dotenv()



app = FastAPI()

# 💡 CORS ayarları burada gəlir
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://apohigh.me",        # frontend domain
        "http://localhost:3000"      # local dev üçün
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/sync-highlights")
def sync_highlights():
    db = SessionLocal()
    save_highlight_matches_to_db(db)
    return {"status": "ok"}


@app.get("/highlights")
async def highlights():
    return await fetch_from_highlightly("/games")

@app.get("/teams")
async def teams():
    return await fetch_from_highlightly("/teams")

app.include_router(index.router, prefix="/api")
app.include_router(live.router, prefix="/api")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(index.router)

templates = Jinja2Templates(directory="app/templates")

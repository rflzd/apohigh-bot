import os
import aiohttp
from dotenv import load_dotenv
from db.base import SessionLocal
from db.models.match import Match

load_dotenv()

API_BASE_URL = "https://soccer.highlightly.net"
API_KEY = os.getenv("RAPIDAPI_KEY")

headers = {
    "x-rapidapi-key": API_KEY,
    "accept": "application/json",
}


async def get_leagues(mode: str, country: str):
    url = f"{API_BASE_URL}/leagues"
    params = {"mode": mode, "country": country}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as resp:
            if resp.status != 200:
                return None
            return await resp.json()


async def get_matches(mode: str, league_id: int, timezone: str = "Asia/Baku"):
    url = f"{API_BASE_URL}/matches"
    params = {"mode": mode, "league_id": league_id, "timezone": timezone}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as resp:
            if resp.status != 200:
                return None
            return await resp.json()


async def get_live_matches():
    return await get_matches(mode="live", league_id=0)


async def get_prematch_matches():
    return await get_matches(mode="prematch", league_id=0)


async def get_match_detail(match_id: int):
    url = f"{API_BASE_URL}/matches/{match_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                return None
            return await resp.json()


async def get_h2h(team1_id: int, team2_id: int):
    url = f"{API_BASE_URL}/head-2-head"
    params = {"teamIdOne": team1_id, "teamIdTwo": team2_id}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as resp:
            if resp.status != 200:
                return None
            return await resp.json()


async def get_odds(match_id: int, odds_type: str = "prematch"):
    url = f"{API_BASE_URL}/odds"
    params = {"matchId": match_id, "type": odds_type}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as resp:
            if resp.status != 200:
                return None
            return await resp.json()


async def get_statistics(match_id: int):
    url = f"{API_BASE_URL}/statistics/{match_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                return None
            return await resp.json()


async def get_lineups(match_id: int):
    url = f"{API_BASE_URL}/lineups/{match_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                return None
            return await resp.json()


async def get_team_statistics(team_id: int, from_date: str):
    url = f"{API_BASE_URL}/teams/statistics"
    params = {"teamId": team_id, "fromDate": from_date}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as resp:
            if resp.status != 200:
                return None
            return await resp.json()

# Verilənlər bazasına matçları əlavə etmək
def insert_matches(matches_data):
    db = SessionLocal()
    for match in matches_data:
        db_match = Match(
            match_id=match['match_id'],
            league_id=match['league_id'],
            home_team=match['home_team'],
            away_team=match['away_team'],
            start_time=match['start_time'],
            status=match['status']
        )
        db.add(db_match)
    db.commit()
    db.close()

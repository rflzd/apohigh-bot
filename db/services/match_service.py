from db.base import SessionLocal
from db.models.match import Match

def insert_matches(matches_data):
    db = SessionLocal()
    try:
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
    finally:
        db.close()

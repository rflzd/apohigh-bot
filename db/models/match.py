from db.db import SessionLocal
from db.models.match import Match

def insert_matches(matches_data):
    db = SessionLocal()  # Verilənlər bazasına qoşuluruq
    for match in matches_data:
        # API-dən gələn hər bir matç üçün Match modelinə uyğun məlumatları əlavə edirik
        db_match = Match(
            match_id=match['match_id'],  # Matçın unikal ID-si
            league_id=match['league_id'],  # Liqanın ID-si
            home_team=match['home_team'],  # Ev sahibi komanda
            away_team=match['away_team'],  # Qonaq komanda
            start_time=match['start_time'],  # Matçın başlama vaxtı
            status=match['status']  # Matçın cari vəziyyəti (canlı və ya bitmiş)
        )
        db.add(db_match)  # Yeni matçı əlavə edirik
    db.commit()  # Dəyişiklikləri saxlayırıq
    db.close()  # Verilənlər bazası əlaqəsini bağlayırıq

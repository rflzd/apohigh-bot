def generate_ai_analysis(match):
    """
    Match obyektindən süni intellekt təhlili verir.
    Hazırda sadə qaydada dummy analiz qaytarır.
    """

    home = match.get("homeTeam", {}).get("name", "Komanda A")
    away = match.get("awayTeam", {}).get("name", "Komanda B")
    odds = match.get("odds", {})

    # Sadə ehtimal və dummy təkliflər
    return (
        f"🤖 *AI Təhlili:*\n"
        f"🏟️ {home} vs {away}\n\n"
        f"📊 *Ehtimal nəzəriyyəsi:* {home} qalib gəlmə şansı: 64%\n"
        f"🧠 *Qeyri-səlis məntiq:* {away} son 5 oyunun 4-də məğlub olub — zəif formadadır.\n"
        f"🎲 *Bukmeyker manipulyasiyası:* Əmsal dəyişikliklərində şübhəli aktivlik görünmür.\n\n"
        f"🎯 *Tövsiyə:* {home} qalib (Mərc növü: 1)"
    )

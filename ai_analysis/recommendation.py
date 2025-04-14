def analyze_bet_coupon(coupon_text: str) -> str:
    """
    Kupon mətni əsasında sadə AI analizi qaytarır.
    Bu sadə dummy versiyadır — istəyə görə statistikaya əsaslanan modellə genişlənə bilər.
    """

    lines = coupon_text.split(",")
    analysis = []

    for line in lines:
        line = line.strip()
        if "-" in line:
            parts = line.split("-")
            team = parts[0].strip()
            bet = parts[1].strip()

            analysis.append(
                f"📌 *{team}*\n"
                f"🎯 Mərc növü: {bet}\n"
                f"📊 Risk dərəcəsi: Orta\n"
                f"✅ AI Tövsiyəsi: Yaxşı seçim görünür\n"
            )
        else:
            analysis.append(f"⚠️ Format uyğun deyil: {line}")

    return "\n\n".join(analysis)

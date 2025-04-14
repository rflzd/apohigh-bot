# utils/flag_to_country.py

def flag_to_country(flag_emoji: str) -> str:
    """
    Emoji şəklindəki bayrağı ölkə koduna çevirir.
    Məsələn: 🇩🇪 → DE
    """
    try:
        return ''.join([chr(ord(char) - 127397) for char in flag_emoji])
    except Exception:
        return "UNKNOWN"

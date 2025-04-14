from countryinfo import CountryInfo

def extract_country_name_from_flag(flag):
    try:
        # 🇹🇷 → TR
        code_points = [ord(char) - 0x1F1E6 + ord('A') for char in flag if '\U0001F1E6' <= char <= '\U0001F1FF']
        country_code = ''.join([chr(cp) for cp in code_points])
        country = CountryInfo(country_code)
        return country.info().get("name")
    except:
        return None

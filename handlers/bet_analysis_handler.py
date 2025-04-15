import pytesseract
from PIL import Image
from telegram import Update
from telegram.ext import ContextTypes
import numpy as np

# Ehtimal hesablaması üçün sadə model
def calculate_probability(odds: float) -> float:
    """Əmsala əsaslanaraq qalib gəlmə ehtimalını hesablayır"""
    return 1 / odds

# Qeyri-səlis məntiq üçün sadə model
def fuzzy_logic(probability: float) -> str:
    """Qeyri-səlis məntiq ilə ehtimalı təhlil edir"""
    if probability > 0.75:
        return "Çox yüksək ehtimal"
    elif probability > 0.5:
        return "Orta ehtimal"
    else:
        return "Aşağı ehtimal"

# Bukmeker əmsallarını təhlil edirik
def analyze_odds(betting_odds: list):
    """Bukmeker əmsallarını təhlil edib ehtimalı hesablamaq"""
    probabilities = [calculate_probability(odds) for odds in betting_odds]
    fuzzy_results = [fuzzy_logic(prob) for prob in probabilities]
    
    return probabilities, fuzzy_results

# OCR ilə kupon analizi
def extract_odds_from_image(image_path: str):
    """Şəkildən əmsalları çıxarır"""
    # Şəkli oxuyuruq
    img = Image.open(image_path)
    
    # OCR istifadə edirik və mətni çıxarırıq
    text = pytesseract.image_to_string(img)
    
    # Sadəlik üçün əmsalları tapırıq
    odds = []
    for word in text.split():
        try:
            odds.append(float(word))
        except ValueError:
            continue
    
    return odds

async def bet_analysis_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        # Şəkli götürürük
        file = await update.message.photo[-1].get_file()
        file_path = await file.download()

        # OCR ilə əmsalları çıxarırıq
        odds = extract_odds_from_image(file_path)

        if not odds:
            await update.message.reply_text("Kupon şəkli üzərində əmsallar tapılmadı.")
            return
        
        # Əmsallar üzərində təhlil edirik
        probabilities, fuzzy_results = analyze_odds(odds)
        
        # Nəticələri istifadəçiyə göndəririk
        result_message = "Kupon analizinin nəticələri:\n"
        for i, odds_val in enumerate(odds):
            result_message += f"Əmsal: {odds_val} | Ehtimal: {probabilities[i]:.2f} | Təhlil: {fuzzy_results[i]}\n"
        
        await update.message.reply_text(result_message)
    else:
        await update.message.reply_text("Zəhmət olmasa bir kupon şəkli göndərin.")

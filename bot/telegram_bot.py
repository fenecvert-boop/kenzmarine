import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from utils.erddap_client import get_sst_at_position

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["SST à position GPS"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Bienvenue sur Kenzmarine !", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "°" in text and "'" in text:
        try:
            lat, lon = parse_ddmm_format(text)
            sst = get_sst_at_position(lat, lon)
            if sst:
                await update.message.reply_text(f"🌊 SST à cette position : {sst} °C")
            else:
                await update.message.reply_text("Aucune donnée disponible.")
        except Exception:
            await update.message.reply_text("Format invalide. Ex : 36°43.520'N 5°04.946'E")
    else:
        await update.message.reply_text("Envoie une position GPS au format : 36°43.520'N 5°04.946'E")

def parse_ddmm_format(gps_text: str):
    import re
    match = re.findall(r"(\d{2})°(\d{2}\.\d+)'([NS])\s*(\d{2,3})°(\d{2}\.\d+)'([EW])", gps_text)
    if not match:
        raise ValueError("Invalid format")
    lat_deg, lat_min, ns, lon_deg, lon_min, ew = match[0]
    lat = int(lat_deg) + float(lat_min) / 60
    lon = int(lon_deg) + float(lon_min) / 60
    if ns == 'S':
        lat *= -1
    if ew == 'W':
        lon *= -1
    return lat, lon

def start_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

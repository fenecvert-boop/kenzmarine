# Kenzmarine v2

Bot Telegram pour récupérer les données océaniques depuis le serveur ERDDAP d'IFREMER.

## 🚀 Installation

```bash
git clone https://github.com/<ton_user>/kenzmarine.git
cd kenzmarine
pip install -r requirements.txt
```

## ⚙️ Configuration

Copie `.env.example` en `.env` et insère ton token :

```env
TELEGRAM_TOKEN=XXXXXX
```

## ▶️ Lancement

```bash
python main.py
```

## 🌊 Fonctionnalité actuelle

- Récupération de la SST (température de surface) pour une position GPS au format `36°43.520'N 5°04.946'E`.
- Format accepté : Degrés + Minutes Décimales.

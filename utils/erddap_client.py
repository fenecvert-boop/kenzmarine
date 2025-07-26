import requests
from datetime import datetime

def get_sst_at_position(lat, lon, depth=0):
    today = datetime.utcnow().strftime("%Y-%m-%dT00:00:00Z")
    url = (
        "https://www.ifremer.fr/erddap/griddap/MEDSEA_MULTIYEAR_PHY_006_004_temperature.json?"
        f"thetao[{today}][{depth}][{lat:.4f}][{lon:.4f}]"
    )
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        return round(data["table"]["rows"][0][0], 2)
    except Exception:
        return None

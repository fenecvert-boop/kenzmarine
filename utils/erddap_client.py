import requests
from datetime import datetime
import urllib.parse

def get_sst_at_position(lat, lon, depth=0):
    today = datetime.utcnow().strftime("%Y-%m-%dT00:00:00Z")
    base_url = "https://www.ifremer.fr/erddap/griddap/MEDSEA_MULTIYEAR_PHY_006_004_temperature.json"
    
    # ⚠️ le bon nom est "thetao"
    query = f"thetao[{today}][{depth}][{round(lat, 2)}][{round(lon, 2)}]"
    encoded_query = urllib.parse.quote(query, safe="[]")
    
    url = f"{base_url}?{encoded_query}"
    
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        return round(data["table"]["rows"][0][0], 2)
    except Exception as e:
        print("ERDDAP error:", e)
        return None

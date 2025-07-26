import requests
from datetime import datetime
import urllib.parse

def get_sst_at_position(lat, lon, depth=0):
    """
    Récupère la température de surface (SST) à partir du serveur ERDDAP IFREMER
    pour une position donnée (latitude, longitude) et une date du jour.
    """

    # Date au format ISO
    today = datetime.utcnow().strftime("%Y-%m-%dT00:00:00Z")

    # Base de l'URL ERDDAP
    base_url = "https://www.ifremer.fr/erddap/griddap/MEDSEA_MULTIYEAR_PHY_006_004_temperature.json"

    # On arrondit les coordonnées à 2 décimales pour coller à la grille du modèle
    lat = round(lat, 2)
    lon = round(lon, 2)

    # Construction de la requête en respectant la syntaxe ERDDAP
    query = f"thetao[{today}][{depth}][{lat}][{lon}]"
    encoded_query = urllib.parse.quote(query, safe="[]")

    # URL finale
    url = f"{base_url}?{encoded_query}"

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()

        # Vérifie si on a bien une valeur dans "rows"
        if data["table"]["rows"]:
            return round(data["table"]["rows"][0][0], 2)
        else:
            return None
    except Exception as e:
        print("ERDDAP error:", e)
        return None

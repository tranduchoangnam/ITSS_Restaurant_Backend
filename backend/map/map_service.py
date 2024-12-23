from backend.core.config import settings
import requests
import urllib.parse
import math
from backend.core.constant import MapLocation
def get_location(input: str):
    if not input:
        return None
    input = urllib.parse.quote(input)
    search_autocomplete = requests.get(
        f"{settings.MAP_API_URL}/place/autocomplete?input={input}&api_key={settings.MAP_API_KEY}&location=21.017184,%20105.784447"
    )
    place_id = search_autocomplete.json().get("predictions")[0].get("place_id")
    location = requests.get(
        f"{settings.MAP_API_URL}/place/detail?place_id={place_id}&api_key={settings.MAP_API_KEY}"
    )
    lat, lng = location.json().get("result").get("geometry").get("location").values()
    return f"{lat},{lng}"

def calculate_distance(location1: str, location2: str):
    if not location1:
        location1 = MapLocation.HUST
    if not location2:
        return None
    
    R = 6371  # Bán kính Trái Đất (km)
    lat1, lon1 = map(math.radians, map(float, location1.split(',')))
    lat2, lon2 = map(math.radians, map(float, location2.split(',')))

    dLat = lat2 - lat1
    dLon = lon2 - lon1

    a = math.sin(dLat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dLon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c
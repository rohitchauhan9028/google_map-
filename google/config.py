import time
import requests

# YOUR GOOGLE API KEY
API_KEY = "YOUR_API_KEY"

# ALL CATEGORY TYPES
TYPES = [
    "restaurant", "store", "hospital", "gym", "school", "bank", "atm",
    "shopping_mall", "cafe", "supermarket", "pharmacy", "hardware_store",
    "electronics_store", "beauty_salon", "clothing_store", "doctor",
    "car_repair", "car_wash", "gas_station", "movie_theater",
    "furniture_store"
]

# ALL COORDINATES (JITNE CHAHO YAHAN ADD KARO)
COORDINATES = [
    (28.7041, 77.1025),
    (28.7056, 77.1083),
    (28.6990, 77.1200)
]

# Safe getter
def safe_get(val, default="N/A"):
    return val if val is not None else default


# Reverse Geocoding – LAT/LONG → AREA NAME
def get_location_name(lat, lng):
    url = (
        f"https://maps.googleapis.com/maps/api/geocode/json"
        f"?latlng={lat},{lng}&key={API_KEY}"
    )
    res = requests.get(url).json()
    results = res.get("results", [])

    if results:
        return results[0].get("formatted_address", "Unknown Place")

    return "Unknown Place"


# Nearby pagination handler
def get_next_page(url):
    items = []

    while True:
        res = requests.get(url).json()
        results = res.get("results", [])
        items.extend(results)

        next_page = res.get("next_page_token")
        if not next_page:
            break

        time.sleep(2)
        url = url + f"&pagetoken={next_page}"

    return items


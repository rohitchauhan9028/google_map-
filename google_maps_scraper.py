import requests
import pandas as pd
import time

API_KEY = "YOUR_API_KEY"

# All categories (jitna chaho add kar sakte ho)
TYPES = [
    "restaurant", "store", "hospital", "gym", "school", "bank", "atm",
    "shopping_mall", "cafe", "supermarket", "pharmacy", "hardware_store",
    "electronics_store", "beauty_salon", "clothing_store", "doctor",
    "car_repair", "car_wash", "gas_station", "movie_theater",
    "furniture_store",
]

# Multiple coordinates (jitne chaho use kar sakte ho)
COORDINATES = [
    (28.7041, 77.1025),
    (28.7056, 77.1083),
]

data_list = []   # final data store

print("\n📌 SCRAPING STARTED…\n")

for lat, lng in COORDINATES:                      # 🔵 FIRST LOOP (Coordinates)
    for place_type in TYPES:                      # 🔵 SECOND LOOP (Categories)
        
        print(f"➡ {place_type} near {lat},{lng}")

        # Nearby Search API
        nearby_url = (
            f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            f"?location={lat},{lng}&radius=2000&type={place_type}&key={API_KEY}"
        )
        nearby_res = requests.get(nearby_url).json()
        results = nearby_res.get("results", [])

        for place in results:                     # 🔵 THIRD LOOP (Results per category)
            place_id = place.get("place_id")

            # Details API
            details_url = (
                f"https://maps.googleapis.com/maps/api/place/details/json"
                f"?place_id={place_id}&key={API_KEY}"
            )
            details_res = requests.get(details_url).json().get("result", {})

            # Save data in list
            data_list.append({
                "name": place.get("name"),
                "category": place_type,
                "address": details_res.get("formatted_address"),
                "phone": details_res.get("formatted_phone_number"),
                "website": details_res.get("website"),
                "rating": place.get("rating"),
                "reviews": place.get("user_ratings_total"),
                "lat": place["geometry"]["location"]["lat"],
                "lng": place["geometry"]["location"]["lng"],
                "maps_url": details_res.get("url"),
                "place_id": place_id
            })

            time.sleep(0.2)   # safety delay

# Convert to DataFrame + Save
df = pd.DataFrame(data_list)
df.drop_duplicates(subset=["place_id"], inplace=True)
df.to_csv("scraped_loop_data.csv", index=False)

print("\n✔ DONE! Saved file: scraped_loop_data.csv")

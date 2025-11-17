import requests
import pandas as pd
import time

from config import API_KEY, TYPES, COORDINATES, safe_get, get_location_name, get_next_page

data_list = []

print("\n📌 SCRAPING STARTED…\n")

for lat, lng in COORDINATES:

    # GET EXACT LOCATION NAME
    location_name = get_location_name(lat, lng)

    print("\n------------------------------------------------------")
    print(f"📍 SEARCHING LOCATION → {location_name}  ({lat}, {lng})")
    print("------------------------------------------------------\n")

    for place_type in TYPES:
        print(f"➡ Searching {place_type} near {location_name}")

        nearby_url = (
            f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            f"?location={lat},{lng}&radius=2000&type={place_type}&key={API_KEY}"
        )

        places = get_next_page(nearby_url)

        for place in places:

            place_id = place.get("place_id")
            if not place_id:
                continue

            details_url = (
                f"https://maps.googleapis.com/maps/api/place/details/json"
                f"?place_id={place_id}&key={API_KEY}"
            )
            details = requests.get(details_url).json().get("result", {})

            opening = details.get("opening_hours", {})

            data_list.append({
                "location_name": location_name,
                "search_lat": lat,
                "search_lng": lng,
                "category": place_type,

                "name": safe_get(details.get("name")),
                "address": safe_get(details.get("formatted_address")),
                "phone": safe_get(details.get("formatted_phone_number")),
                "website": safe_get(details.get("website")),
                "rating": safe_get(details.get("rating")),
                "reviews": safe_get(details.get("user_ratings_total")),
                "open_now": safe_get(opening.get("open_now")),
                "weekday_text": safe_get(opening.get("weekday_text")),

                "place_lat": place["geometry"]["location"]["lat"],
                "place_lng": place["geometry"]["location"]["lng"],
                "maps_url": safe_get(details.get("url")),
                "place_id": place_id,
            })

            time.sleep(0.2)

# SAVE OUTPUT
df = pd.DataFrame(data_list)
df.drop_duplicates(subset=["place_id"], inplace=True)

df.to_csv("scraped_google_data.csv", index=False)
df.to_excel("scraped_google_data.xlsx", index=False)

print("\n✔ DONE! SAVED:")
print("→ scraped_google_data.csv")
print("→ scraped_google_data.xlsx")



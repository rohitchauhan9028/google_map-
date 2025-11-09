import requests, csv, time


API_key = "Your_Google_Places_API_Key"
location = "Your_Location" # e.g., "37.7749,-122.4194" for San Francisco
radius = 2000 # in meters
keywords = ["restaurant", "cafe", "bar"]
output_csv = "places_output.csv" # output file name

def place_search(API_key, location, radius, keyword, pagetoken=None):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": API_key,
        "location": location,
        "radius": radius,
        "keyword": keyword,
    }
    if pagetoken:
        params["pagetoken"] = pagetoken
    response = requests.get(url, params = params)
    return response.json()
def get_place_details(API_key, place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "key": API_key,
        "place_id": place_id,
        "fields":  "name, formatted_address, formattes_phone_number, website, rating, geometry, opening_hours",

    }
    r = requests.get(url, params = params, timeout = 30)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    rows = []
    resp = place_search(API_key, location, radius, keywords[0])
    while True:
        for result in resp.get("results", []):
            place_id = result.get("place_id")
            details = get_place_details(API_key, place_id).get("result", {})
            rows.append({
                "name": details.get("name") or result.get("name"),
                "address": details.get("formatted_address") or result.get("vicinity"),
                "phone": details.get("formatted_phone_number") or result.get("formatted_phone_number"),
                "website": details.get("website") or result.get("website"),
                "rating": details.get("rating") or result.get("rating"),
                "location": details.get("geometry", {}).get("location") or result.get("geometry", {}).get("location"),


            })
            time.sleep(1) # To respect API rate limits
            # handle pagination token 
            pagetoken = resp.get("next_page_token")
            if not pagetoken:
                break
            time.sleep(2) # wait before making the next request
            resp = place_search(API_key, location, radius, keywords[0], pagetoken)
    # save to csv
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {len(rows)} places to {output_csv}")




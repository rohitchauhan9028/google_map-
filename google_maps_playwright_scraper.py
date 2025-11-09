from playwright.sync_api import sync_playwright
import csv
import time

Search_Query = "coffee ShopeS"
output  = "google_maps_playwright_output.csv"
MAX_Results = 40

def scrape_google_maps(query, max_results=50):
    result = []
    with sync_playwright() as p:
        browser = p.chromium.launch(handless = True)
        page = browser.new_page()
        page.goto("https://www.google.com/maps", timeout=60000)
        page.wait_for_load_state("input[aria-label='Search Google Maps'], input[aria-label='Search']", timeout=60000)
        # Choose whichever selector works 
        try:
            search_input = page.query_selector("input[  aria-label='Search Google Maps']")
        except:
            search_input = page.query_selector("input[aria-label='Search']")
        if not  search_input:
            print("search input not  found- page layout may have changed")
        
        search_input.click()
        search_input.fill(query)
        search_input.press("Enter")
        # Wait for results to load
        page.wait_for_load_state("div[role='article'], div['aria*=Result for'], div.section-result, .Nv2PK  ", timeout=60000)

        # scroll to load more results
        sidebar = page.query_selector("div[role='region']")
        if not sidebar:
             sidbar = page
        
        collected = 0
        seen_place_urls = set()
        # scroll loop (scroll the  sidbar to  load more results)
        for _scroll_attempt in range(20):
               page = page.query_selector_all("div[role='article'], a[href*='/place/'], .Nv2PK")
               for place in page:
                     try:
                          title_elem = place.query_selector("h3 span, .qBF1Pd, .hfpxzc")
                          title_elem = title_elem.inner_text().strip() if title_elem else "N/A"
                          link_elem = place.query_selector("a[href*='/place/'], a")
                          link_elem = link_elem.get_attribute("href") if link_elem else "N/A"
                          if link_elem in seen_place_urls:
                                continue
                          try:
                               place.click()
                          except:
                               if link_elem :
                                    link_elem.click()
                          page.wait_for_timeout(1200)
                    # extract details from detail pane
                          name = page.query_selector("h1 span")  # often the name is in h1 span
                          phone = page.query_selector("button[data-tooltip='Copy phone number'], button[aria-label*='call']")
                          address = page.query_selector("button[data-tooltip='Copy address'], button[aria-label*='Copy address'], span[jsaction][data-item-id='address']")
                          rating = page.query_selector("div[aria-label*='stars'], .F7nice")
                          website = page.query_selector("a[data-tooltip='Open website']")

                          rec = {
                            "title": title_elem or (name.inner_text().strip() if name else None),
                            "href": link_elem,
                             "address": address.inner_text().strip() if address else None,
                             "phone": phone.get_attribute("aria-label").replace("Phone: ", "").strip() if phone and phone.get_attribute("aria-label") else (phone.inner_text().strip() if phone else None),
                            "rating": rating.get_attribute("aria-label") if rating and rating.get_attribute("aria-label") else (rating.inner_text().strip() if rating else None),
                             "website": website.get_attribute("href") if website else None,
                               
                          }
                          result.append(rec)
                          seen_place_urls.add(link_elem)
                          collected += 1
                          if collected >= max_results:
                               break
                     except Exception as e:
                            pass
                     if collected >= max_results:
                          break
        try:
            page.keyboard.down("PageDown")
            page.wait_for_timeout(1000)
        except:
            pass
    browser.close()
    return result
if __name__ == "__main__":
    Search_Query = "restaurants"
    data =  scrape_google_maps(Search_Query, MAX_Results)
    if data:
     

        keys = list(data[0].keys())
        with open(output, "w", newline="", encoding="utf-8") as f:
            import csv
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        print(f"Wrote {len(data)} rows to {output}")
    else:
        print("No data scraped; adjust selectors or debug with headless=False")
     
     
              
              
                          
                          
                        
                          
                          

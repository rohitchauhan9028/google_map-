from playwright.sync_api import sync_playwright
import time, random
import csv # Added for saving results

def human_sleep(a=1.2, b=2.8):
    """Pauses execution for a random period to mimic human behavior."""
    time.sleep(random.uniform(a, b))

def run_scraper(search_term, log_callback):
    """
    The main scraping function that executes Playwright logic.

    Args:
        search_term (str): The keyword to search on Google Maps.
        log_callback (function): A function (from the GUI) to output messages.
    """
    # ---------------------------------------
    # COORDINATES YOU WANT TO SCRAPE (Original List)
    # ---------------------------------------
    coords = [
        (28.8542, 76.8634),
        (28.8542, 76.9143),
        (28.8542, 76.9652),
        (28.8066, 76.9652),
    ]
    results_final = []
    browser = None
    
    try:
        with sync_playwright() as p:
            # Set headless=True so the browser runs in the background for the GUI
            browser = p.chromium.launch(
            headless=True,
            proxy={
            "server": "http://IP:PORT",
            "username": "PROXY_USER",
            "password": "PROXY_PASS"
            }
            )
            page = browser.new_page()
            
            # Add a header row
            results_final.append(
                ['Name', 'Rating', 'Address', 'Phone', 'Website', 'Lat', 'Lng']
            )

            for lat, lng in coords:
                log_callback(f"\n==============================")
                log_callback(f"🔵 Scraping coord → {lat}, {lng}")
                log_callback("==============================")

                # 1. OPEN MAP AT COORDINATE
                maps_url = f"https://www.google.com/maps/@{lat},{lng},15z"
                page.goto((maps_url), timeout=60000)
                human_sleep(2, 3)

                # 2. SEARCH KEYWORD
                log_callback(f"🔍 Searching '{search_term}'...")
                search = page.get_by_role("combobox", name="Search Google Maps")
                search.click()
                search.fill(search_term) # Use the search term provided by the UI
                page.keyboard.press("Enter")
                human_sleep(4, 6)

                # 3. Only first 2 cards (your original logic)
                cards = page.locator('div[role="article"]')

                cards.first.wait_for(timeout=10000)  # WAIT here

                total = min(cards.count(), 2)

                for i in range(total):
                    log_callback(f"\n➡ Opening business {i+1}...")
                    cards.nth(i).click()
                    human_sleep(2, 3)

                    # Extract business info (YOUR ORIGINAL SELECTORS)
                    try: name = page.locator(".DUwDvf.lfPIob").inner_text()
                    except: name = "N/A"
                    try: rating = page.locator("span[aria-label*='stars']").first.inner_text()
                    except: rating = "N/A"
                    try: address = page.locator("button[data-item-id='address']").inner_text()
                    except: address = "N/A"
                    try: phone = page.locator("button[data-item-id='phone']").inner_text()
                    except: phone = "N/A"
                    try: 
                        website = page.locator("a[data-item-id='authority']").first.get_attribute("href")
                        if not website: website = "N/A"
                    except: website = "N/A"

                    extracted = [name, rating, address, phone, website, str(lat), str(lng)]
                    results_final.append(extracted)
                    log_callback(f"📌 Extracted: {extracted}")

                    # close panel
                    page.keyboard.press("Escape")
                    human_sleep(1.5, 2.5)
            
            # Save results to a CSV file
            with open('google_maps_results.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(results_final)

            log_callback("\n🎉 SCRAPING COMPLETE!")
            log_callback("Data saved to: google_maps_results.csv")
            return True

    except Exception as e:
        log_callback(f"\n🛑 An error occurred: {e}")
        return False

    

if __name__ == '__main__':
    # This block allows you to test the scraper logic without the GUI
    def console_log(message):
        print(message)
    
    print("Running maps_scraper.py directly for testing...")
    run_scraper('coffee shop', console_log)
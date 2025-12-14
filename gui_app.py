# gui_app.py

import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
from scraper.maps_scraper import run_scraper # Import the core function!

class ScraperApp:
    def __init__(self, master):
        self.master = master
        master.title("Google Maps Scraper UI")

        # Set up a simple grid layout
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)

        # --- Setup GUI Components ---
        
        # 1. Search Term Input
        tk.Label(master, text="Search Term:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.search_entry = tk.Entry(master, width=40)
        self.search_entry.insert(0, "gym") # Default to your original search term
        self.search_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        # 2. Scrape Button
        self.scrape_button = tk.Button(master, text="Start Scraper", command=self.start_scraping_thread)
        self.scrape_button.grid(row=1, column=0, columnspan=2, pady=10)

        # 3. Results/Log Display
        tk.Label(master, text="Scraper Output:").grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky='w')
        self.results_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=80, height=20)
        self.results_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # --- Methods ---

    def log_output(self, message):
        """Method to safely write messages to the GUI text box."""
        # Use Tkinter's after method for thread-safe updates if needed, 
        # but for simple logging, direct update usually works fine.
        self.results_text.insert(tk.END, message + "\n")
        self.results_text.see(tk.END) # Auto-scroll
        self.master.update()

    def start_scraping_thread(self):
        """Initiates the scraping process in a background thread."""
        self.results_text.delete(1.0, tk.END)
        self.log_output("--- Scraper Initializing... Please wait... ---")
        
        # Disable button and set status
        self.scrape_button.config(state=tk.DISABLED, text="Scraping Running...")

        # Start the scraping logic in a new thread
        self.scraper_thread = threading.Thread(target=self.run_scraper_logic)
        self.scraper_thread.start()

    def run_scraper_logic(self):
        """The function executed by the separate thread."""
        search_term = self.search_entry.get()
        
        # Call the external scraping function from maps_scraper.py
        success = run_scraper(search_term, self.log_output)
        
        # Re-enable the button
        self.scrape_button.config(state=tk.NORMAL, text="Start Scraper")
        
        if success:
          self.master.after(0, lambda: messagebox.showinfo(
          "Success",
          "Scraping completed and data saved!"
    ))
        else:
           self.master.after(0, lambda: messagebox.showerror(
           "Error",
           "Scraping failed. Check logs."
           ))

if __name__ == '__main__':
    root = tk.Tk()
    app = ScraperApp(root)
    root.mainloop()
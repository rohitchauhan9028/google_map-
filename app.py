from flask import Flask, render_template, request
from scraper.maps_scraper import run_scraper

app = Flask(__name__)

def web_log(message):
    print(message)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        search_term = request.form["search"]
        run_scraper(search_term, web_log)
        return "Scraping finished! Check CSV file."
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

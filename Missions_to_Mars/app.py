# import necessary libraries
from flask import Flask, render_template
from Scrape_Mars import scrape

# Initialize your Flask app here
app = Flask(__name__)

# Create a route, view function that takes in a list of strings and renders index.html template
@app.route("/")
def index():
    mars_attacks = 'hello Q'
    return render_template("index.html", thing=mars_attacks)

@app.route("/scrape")
def do_scape():
    scrape()
    return 'scrape complete'
    
if __name__ == "__main__":
    app.run(debug=True)
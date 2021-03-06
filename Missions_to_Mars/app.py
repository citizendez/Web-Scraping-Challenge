# import necessary libraries
from flask import Flask, redirect, url_for, render_template, request
from Scrape_Mars import scrape
import pymongo

# Initialize your Flask app here
app = Flask(__name__)

# Create a route, view function that takes in a list of strings and renders index.html template
@app.route("/")
def index():
    # Initialize PyMongo to work with MongoDBs
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    # Define database and collection
    db = client.mars_db
    features = db.features.find()
    feature = features[0]
    articles = db.articles.find()
    return render_template('index.html', feature=feature, articles=articles)
    
# create rout for scraping
@app.route("/scrape")
def do_scape():
    scrape()
    return render_template('scrape.html')
    
if __name__ == "__main__":
    app.run(debug=True)
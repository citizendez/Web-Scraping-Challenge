# import necessary libraries
from flask import Flask, render_template
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
    return render_template('index.html', feature=feature)
    

@app.route("/scrape")
def do_scape():
    scrape()
    return 'scrape complete'
    
if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    #Find one record of data from the mongo database
    mars_info= mongo.db.mars_info.find_one()
    return render_template("index.html", mars_info_dict=mars_info_dict)

#Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    mars_info = scrape_mars.scrap_data()

    mongo.db.mars_info.update({}, mars_info, upsert=True)

    return redirect("/", code=302)
    
if __name__ == "__main__":
    app.run(debug=True)
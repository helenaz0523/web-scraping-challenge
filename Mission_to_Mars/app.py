from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)


conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_data


@app.route("/")
def index():
    db_list = client.list_database_names()
    if "mars_data" in db_list:
        mars_stuff = list(db.collection.find())[0]
        return  render_template('index.html', mars_stuff=mars_stuff)
    else:    
        return  render_template('index_scrape_only.html')


@app.route("/scrape")
def scrape():
    db.collection.delete_many({})
    mars_new_scrap = scrape_mars.scrap_data_mongo()
    db.collection.insert_one(mars_new_scrap)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
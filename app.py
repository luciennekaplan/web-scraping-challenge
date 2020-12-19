from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scrape as ms

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
collection = mongo.db.mars

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_info = collection.find_one()

    # Return template and data
    return render_template("index.html", mars= mars_info)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function and save the results to a variable
    mars_info = ms.scrape()

    # Update the Mongo database using update and upsert=True
    collection.update(
        {}, 
        mars_info,
        upsert=True
    )


    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)


from flask import Flask,render_template,jsonify,request
import logging
import pymongo.mongo_client
import pymongo


app = Flask(__name__)

logging.basicConfig(filename="info.log", level=logging.INFO)

try:
    # MongoDB connection setup
    client = pymongo.MongoClient("mongodb+srv://ronak:pwskills@cluster0.uelexi3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["task_python1"]
    collection = db["details"]
    logging.info("Connected to MongoDB and collection created")
except Exception as e:
    logging.error(f"Error connecting to MongoDB: {e}")


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["GET", "POST"])
def data():
    if request.method == "POST":
        try:
            # Retrieve form data
            firstname = request.form.get("FirstName")
            lastname = request.form.get("LastName")
            number = request.form.get("Number")
            mail = request.form.get("Email")

            # Basic form validation
            if not firstname or not lastname or not number or not mail:
                raise ValueError("All fields are required.")

            # Insert data into MongoDB
            mydata = {"FirstName": firstname, "LastName": lastname, "Number": number, "Email": mail}
            collection.insert_one(mydata)
            logging.info("Data stored in MongoDB")
        except ValueError as ve:
            logging.error(f"Form validation error: {ve}")
        except Exception as e:
            logging.error(f"Error processing form data: {e}")
            return "An error occurred while processing form data"

    try:
        # Retrieve all data from MongoDB collection
        data = list(collection.find())
        logging.info("Data retrieved from MongoDB")
        return render_template("result.html", data=data)
    except Exception as e:
        logging.error(f"Error fetching data from MongoDB: {e}")
        return "An error occurred while fetching data"


@app.route("/result" ,methods=["GET","POST"])
def result():
    try:
        # Retrieve all data from MongoDB collection
        data = list(collection.find())
        logging.info("Data retrieved from MongoDB")
        return render_template("result.html", data=data)
    except Exception as e:
        logging.error(f"Error fetching data from MongoDB: {e}")
        return "An error occurred while fetching data"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
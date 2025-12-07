from flask import Flask, jsonify, render_template, request, redirect, url_for
from dotenv import load_dotenv
import json
import pymongo
import os

# Load environment variables
load_dotenv()

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("Error: MONGO_URI not found in environment variables!")

import certifi
client = pymongo.MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    tlsAllowInvalidCertificates=True
)
db = client['test']
collection = db['flask_tutorial']

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submitdata():
    try:
        # Get form data
        formdata = dict(request.form)

        # Insert into MongoDB
        result = collection.insert_one(formdata)

        if result.inserted_id:
            return redirect(url_for('success'))

    except Exception as e:
        # Show error on same page
        return render_template('index.html', error=str(e))

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    item_name = request.form.get('itemName')
    item_description = request.form.get('itemDescription')

    if not item_name or not item_description:
        return jsonify({"error": "Missing fields"}), 400

    data = {
        "itemName": item_name,
        "itemDescription": item_description
    }

    collection.insert_one(data)

    return jsonify({"message": "To-Do Item Saved Successfully!"}), 201


if __name__ == '__main__':
    app.run(debug=True)

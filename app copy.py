from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import pymongo
from bson import ObjectId

load_dotenv()

# -------------------------
# MongoDB Connection
# -------------------------
MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)
db = client['test']
collection = db['flask_tutorial']

# -------------------------
# Flask App
# -------------------------
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


# -------------------------
# Signup API (Fixed)
# -------------------------
@app.route('/signup', methods=['POST'])
def signup():

    # Get form data
    formdata = dict(request.form)

    # Insert into DB
    result = collection.insert_one(formdata)

    # Convert ObjectId to string for JSON
    formdata['_id'] = str(result.inserted_id)

    return jsonify({
        "status": "success",
        "data": formdata
    })

# --------------------------
# View User Data
# -------------------------
@app.route('/user_list')
def user_list():
    usersData = collection.find()
    usersData = list(usersData)
    for user in usersData:
        print(user)
        del user['_id']

    return usersData



# -------------------------
# API Route (Fixed)
# -------------------------
@app.route('/api/<a>/<b>/<c>')
def calculate(a, b, c):
    calculation = int(a) * int(b) * int(c)

    return jsonify({
        "calculation": calculation
    })


# -------------------------
# Run App
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)

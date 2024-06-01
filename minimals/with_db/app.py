from flask import Flask, jsonify, render_template
from pymongo import MongoClient
from bson import json_util
import requests
import itertools
import string
import logging

app = Flask(__name__)
client = MongoClient("mongodb://mongo:27017/")
db = client.bucket_status_db
collection = db.results

def generate_bucket_names(length=5):
    chars = string.ascii_lowercase  # Use only lowercase letters
    for name in itertools.product(chars, repeat=length):
        yield ''.join(name)

def check_s3_bucket_status(bucket_name, timeout=0.1):
    url = f'http://{bucket_name}.s3.amazonaws.com'
    try:
        response = requests.head(url, timeout=timeout)
        return response.status_code
    except requests.exceptions.Timeout:
        return 'Timeout'
    except requests.exceptions.RequestException as e:
        return str(e)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/check/buckets/v1', methods=['GET'])
def check_buckets():
    results = []
    for bucket_name in generate_bucket_names():
        if len(results) >= 10:
            break
        status_code = check_s3_bucket_status(bucket_name)
        if str(status_code).startswith(('2', '3')) or status_code == 403:
            result = {
                "name": f"http://{bucket_name}.s3.amazonaws.com",
                "status_code": status_code
            }
            insert_result = collection.insert_one(result)
            result['_id'] = str(insert_result.inserted_id)  # Convert ObjectId to string
            results.append(result)
    return jsonify(results)

@app.route('/check/buckets/db/v1', methods=['GET'])
def get_buckets_from_db():
    results = list(collection.find({}, {'_id': 0}))
    return json_util.dumps(results)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/help')
def help():
    return render_template("help.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

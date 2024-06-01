from flask import Flask, jsonify, render_template
from bson import json_util
from bucket_manager import generate_bucket_names, check_s3_bucket_status
from database import insert_result, collection

app = Flask(__name__)

@app.route('/check/buckets/v1', methods=['GET'])
def check_buckets():
    results = []
    for bucket_name in generate_bucket_names():
        status_code = check_s3_bucket_status(bucket_name)
        if str(status_code).startswith(('2', '3')) or status_code == 403:
            result = {
                "name": f"http://{bucket_name}.s3.amazonaws.com",
                "status_code": status_code
            }
            insert_id = insert_result(result)  # Ensure MongoDB ID is handled correctly
            if insert_id:
                result['_id'] = insert_id  # Convert ObjectId to string
            results.append(result)
        if len(results) >= 5:  # You may want to adjust this if needed
            break
    if not results:
        return jsonify({"error": "No buckets with status code 2xx, 3xx, or 403 found."}), 404
    return jsonify(results)

@app.route('/check/buckets/db/v1', methods=['GET'])
def get_buckets_from_db():
    results = list(collection.find({}, {'_id': 0}))
    return json_util.dumps(results)  # Correctly using json_util to handle Mongo objects

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/help')
def help():
    return render_template("help.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

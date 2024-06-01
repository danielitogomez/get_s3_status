from flask import Flask, jsonify, render_template
import requests
import itertools
import string

app = Flask(__name__)

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

@app.route('/check/buckets/v1', methods=['GET'])
def check_buckets():
    results = []
    for bucket_name in generate_bucket_names():
        if len(results) >= 10:
            break
        status_code = check_s3_bucket_status(bucket_name)
        results.append({"name": f"http://{bucket_name}.s3.amazonaws.com", "status_code": status_code})
    return jsonify(results)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/help')
def help():
    return render_template("help.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

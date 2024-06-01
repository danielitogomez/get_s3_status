import requests
import itertools
import string
import logging

# Setup basic logging
logging.basicConfig(level=logging.DEBUG)

# Toggle: Set to 'aaaaw' to test with this specific bucket, or None to generate names
test_bucket_name = ''

def generate_bucket_names():
    if test_bucket_name:
        # Only yield this specific bucket for testing
        yield test_bucket_name
    else:
        # Use only lowercase letters and generate combinations of length 5
        chars = string.ascii_lowercase
        for name in itertools.product(chars, repeat=5): # iterations for 5 characters
            yield ''.join(name)

def check_s3_bucket_status(bucket_name, timeout=0.1): # Timeout of 0.1 s just for PoC
    url = f'http://{bucket_name}.s3.amazonaws.com'
    try:
        # Using GET request method
        response = requests.get(url, timeout=timeout)
        logging.debug(f"Checked URL {url}, received status code: {response.status_code}")
        return response.status_code
    except requests.exceptions.Timeout:
        logging.error(f"Timeout occurred when checking URL: {url}")
        return 'Timeout'
    except requests.exceptions.RequestException as e:
        logging.error(f"Request exception when checking URL {url}: {str(e)}")
        return str(e)

import requests
import itertools
import string

#def generate_bucket_names():
#    # Directly yield the specific bucket name 'aaaaw' for testing
#    yield 'aaaaw'

def generate_bucket_names():
    chars = string.ascii_lowercase  # Use only lowercase letters
    for name in itertools.product(chars, repeat=5):  # Generate combinations of length 5
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

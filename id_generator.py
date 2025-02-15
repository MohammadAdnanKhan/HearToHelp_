import base64
import os

def generate_random_string():
    random_bytes = os.urandom(6)
    random_base64_string = base64.urlsafe_b64encode(random_bytes).decode('utf-8')
    return random_base64_string

from requests.auth import HTTPBasicAuth

base_url = 'http://127.0.0.1:5000/'

correct_auth = HTTPBasicAuth('user', 'test_keypass')
wrong_auth = HTTPBasicAuth('user', 'false_keypass')
import requests
from requests.auth import HTTPBasicAuth

url = 'http://127.0.0.1:5000/save/'

def test_save_ok():
    response = requests.get(url, auth=HTTPBasicAuth('user', 'test_keypass'))
    assert response.status_code == 200

def test_save_ko_no_auth():
    response = requests.get(url)
    assert response.status_code == 401

def test_save_ko_auth_false():
    response = requests.get(url, auth=HTTPBasicAuth('user', 'false_keypass'))
    assert response.status_code == 401
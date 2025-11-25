import requests
from requests.auth import HTTPBasicAuth

import tests

url = tests.base_url + 'save/'

# GET /save/

def test_get_save_ok():
    response = requests.get(url, auth=tests.correct_auth)
    assert response.status_code == 200

# POST /save/

post_data = {
    'author': 'Erwan',
    'title': 'My saved post',
    'content': 'This is a test post'
}

def test_post_save_ok():
    response = requests.post(url, auth=tests.correct_auth, json=post_data)
    assert response.status_code == 200

def test_post_save_ko_no_json():
    response = requests.post(url, auth=tests.correct_auth, data=post_data)
    assert response.status_code == 415

def test_post_save_ko_no_auth():
    response = requests.post(url)
    assert response.status_code == 401

def test_post_save_ko_auth_false():
    response = requests.post(url, auth=tests.wrong_auth)
    assert response.status_code == 401

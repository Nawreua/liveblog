import requests

import tests

url = tests.base_url + 'view/'

# GET /

def test_index_ok():
    response = requests.get(tests.base_url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5

# GET /view/<id>

def test_view_id_ok():
    response = requests.get(url + '1')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 1

def test_view_id_ko():
    response = requests.get(url + '999')
    assert response.status_code == 404

# GET /view/

def test_view_ok():
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 25
    assert data[0]['id'] == 1

def test_view_ok_only_one():
    response = requests.get(url, params={'limit': 1})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['id'] == 1

def test_view_ok_offset():
    response = requests.get(url, params={'offset': 1})
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == 2

def test_view_ok_no_posts():
    response = requests.get(url, params={'offset': 999})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0

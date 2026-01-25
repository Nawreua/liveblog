from app.views import return_html

def test_ko_accept_empty():
    assert not return_html('')

def test_ko_accept_json():
    assert not return_html('application/json')
    assert not return_html('.json')
    assert not return_html('image/*,application/json,.json')

def test_ok_accept_html():
    assert return_html('text/html')
    assert return_html('.htm')
    assert return_html('.html')
    assert return_html('image/*,text/html,.htm')

def test_ok_accept_html_first():
    assert return_html('text/html,application/json')
    assert return_html('image/*,text/html,application/json')
    assert return_html('image/*,text/html,.json')
    assert return_html('image/*,.html,.json')

def test_ko_accept_json_first():
    assert not return_html('application/json,text/html')
    assert not return_html('image/*,application/json,text/html')
    assert not return_html('image/*,.json,text/html')
    assert not return_html('.json,image/*,.html')

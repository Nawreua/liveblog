from app.auth import hash_keypass

def test_hash_simple():
    assert hash_keypass('test_keypass') == '44ea01b1aede885735cb3284076137543f7a264cbddc527fc1c8af2116bf6cd7'
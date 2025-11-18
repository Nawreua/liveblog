"""
A submodule handling all our authentification needs
"""

import os
from hashlib import sha256
from functools import wraps

from flask import request

global_keypass = os.environ.get('GLOBAL_KEYPASS', '')
"""
The global keypass used throughout the app

Use the GLOBAL_KEYPASS environment variable
"""

def hash_keypass(keypass):
    """
    Hash the keypass the user sent us using SHA256
    """
    return sha256(keypass.encode()).hexdigest()

# Based on [Basic Authentication in Flask | Protected Routes](https://www.youtube.com/watch?v=4abHEvWwWPM&t=426s)
def check_auth(keypass):
    """
    Authentification verification function

    If the GLOBAL_KEYPASS was not set, return false
    """
    if global_keypass == '':
        return False
    return hash_keypass(keypass) == global_keypass

def require_auth(f):
    """
    Decorator handling the basic authentification for blogposting
    """
    wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.password):
            return 'Unauthorized', 401
        return f(*args, **kwargs)
    return decorated
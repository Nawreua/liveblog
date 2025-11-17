import os
from app import app, parse_and_config

if __name__ == "__main__":
    parse_and_config()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

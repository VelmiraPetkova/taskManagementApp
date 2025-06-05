from config import create_app
from flask_cors import CORS

from db import db

app= create_app()
CORS(app)

with app.app_context():
    db.init_app(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)



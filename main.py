from config import create_app
from flask_cors import CORS

from db import db

app= create_app()
CORS(app)

with app.app_context():
    db.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)



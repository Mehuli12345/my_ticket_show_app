from flask import Flask
from backend.models import db
from backend.controllers import register_routes


def create_app():
    app = Flask(__name__)
    app.secret_key = 'this_is_my_secret_key'  # ✅ REQUIRED FOR SESSION
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticket_show.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # Allow all domains for CORS

    from .routes import main
    app.register_blueprint(main)

    return app
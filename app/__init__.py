from flask import Flask
from app.database import setup_db
from app.routes import routes

def create_app():
    app = Flask(__name__)
    
    # Database setup
    setup_db()
    
    # Register Blueprints
    app.register_blueprint(routes)

    return app

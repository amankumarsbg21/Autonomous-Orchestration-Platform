from flask import Flask
from app.controllers.chat_controller import chat_bp
from flask_cors import CORS
def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    # Register blueprints (Controllers)
    app.register_blueprint(chat_bp, url_prefix='/api')
    
    return app
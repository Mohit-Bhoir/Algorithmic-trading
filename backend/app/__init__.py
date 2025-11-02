"""
Application Factory for Algorithmic Trading Platform
"""
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from backend.config import config

def create_app(config_name='default'):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    from .models import db, bcrypt
    db.init_app(app)
    bcrypt.init_app(app)
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Initialize CORS
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    
    # Initialize migrations
    migrate = Migrate(app, db)
    
    # Register routes
    from .routes import init_routes
    init_routes(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    @app.route('/')
    def index():
        return {'message': 'Algorithmic Trading Platform API', 'status': 'running'}, 200
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    
    return app

"""
Routes initialization module
"""
from flask import Blueprint

def init_routes(app):
    """Initialize all routes"""
    from .auth import auth_bp
    from .strategies import strategies_bp
    from .backtests import backtests_bp
    from .subscriptions import subscriptions_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(strategies_bp)
    app.register_blueprint(backtests_bp)
    app.register_blueprint(subscriptions_bp)

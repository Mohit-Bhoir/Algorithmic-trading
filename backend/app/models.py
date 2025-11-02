"""
Database Models for Algorithmic Trading Platform
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import JSON

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    """User model for authentication and authorization"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Subscription information
    subscription_tier = db.Column(db.String(50), default='free')
    subscription_start_date = db.Column(db.DateTime)
    subscription_end_date = db.Column(db.DateTime)
    stripe_customer_id = db.Column(db.String(100))
    stripe_subscription_id = db.Column(db.String(100))
    
    # Relationships
    strategies = db.relationship('Strategy', backref='user', lazy=True, cascade='all, delete-orphan')
    backtests = db.relationship('Backtest', backref='user', lazy=True, cascade='all, delete-orphan')
    broker_credentials = db.relationship('BrokerCredential', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'subscription_tier': self.subscription_tier,
            'subscription_start_date': self.subscription_start_date.isoformat() if self.subscription_start_date else None,
            'subscription_end_date': self.subscription_end_date.isoformat() if self.subscription_end_date else None,
            'created_at': self.created_at.isoformat()
        }

class Strategy(db.Model):
    """Trading strategy model"""
    __tablename__ = 'strategies'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'SMA', 'MeanReversion', 'ML'
    parameters = db.Column(JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=False)
    
    # Relationships
    backtests = db.relationship('Backtest', backref='strategy', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert strategy to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'type': self.type,
            'parameters': self.parameters,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_active': self.is_active
        }

class Backtest(db.Model):
    """Backtest results model"""
    __tablename__ = 'backtests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    strategy_id = db.Column(db.Integer, db.ForeignKey('strategies.id'), nullable=False)
    symbol = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    performance = db.Column(db.Float)
    outperformance = db.Column(db.Float)
    results_data = db.Column(JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert backtest to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'strategy_id': self.strategy_id,
            'symbol': self.symbol,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'performance': self.performance,
            'outperformance': self.outperformance,
            'results_data': self.results_data,
            'created_at': self.created_at.isoformat()
        }

class BrokerCredential(db.Model):
    """Broker API credentials model"""
    __tablename__ = 'broker_credentials'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    broker_name = db.Column(db.String(50), nullable=False)  # 'oanda', 'ibkr', 'fxcm'
    api_key = db.Column(db.String(200))
    api_secret = db.Column(db.String(200))
    account_id = db.Column(db.String(100))
    is_demo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert broker credential to dictionary (without exposing secrets)"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'broker_name': self.broker_name,
            'account_id': self.account_id,
            'is_demo': self.is_demo,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class TradingSession(db.Model):
    """Live trading session model"""
    __tablename__ = 'trading_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    strategy_id = db.Column(db.Integer, db.ForeignKey('strategies.id'), nullable=False)
    broker_credential_id = db.Column(db.Integer, db.ForeignKey('broker_credentials.id'), nullable=False)
    status = db.Column(db.String(20), default='stopped')  # 'running', 'stopped', 'error'
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    total_trades = db.Column(db.Integer, default=0)
    total_profit = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert trading session to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'strategy_id': self.strategy_id,
            'broker_credential_id': self.broker_credential_id,
            'status': self.status,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'total_trades': self.total_trades,
            'total_profit': self.total_profit,
            'created_at': self.created_at.isoformat()
        }

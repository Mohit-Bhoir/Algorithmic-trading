"""
Strategy Routes for Algorithmic Trading Platform
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Strategy, User
from datetime import datetime

strategies_bp = Blueprint('strategies', __name__, url_prefix='/api/strategies')

@strategies_bp.route('', methods=['GET'])
@jwt_required()
def get_strategies():
    """Get all strategies for current user"""
    current_user_id = get_jwt_identity()
    strategies = Strategy.query.filter_by(user_id=current_user_id).all()
    
    return jsonify([strategy.to_dict() for strategy in strategies]), 200

@strategies_bp.route('/<int:strategy_id>', methods=['GET'])
@jwt_required()
def get_strategy(strategy_id):
    """Get a specific strategy"""
    current_user_id = get_jwt_identity()
    strategy = Strategy.query.filter_by(id=strategy_id, user_id=current_user_id).first()
    
    if not strategy:
        return jsonify({'error': 'Strategy not found'}), 404
    
    return jsonify(strategy.to_dict()), 200

@strategies_bp.route('', methods=['POST'])
@jwt_required()
def create_strategy():
    """Create a new strategy"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('name') or not data.get('type') or not data.get('parameters'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check subscription limits
    from backend.config import config
    tier_config = config['default'].SUBSCRIPTION_TIERS.get(user.subscription_tier, {})
    max_strategies = tier_config.get('max_strategies', 1)
    
    if max_strategies != -1:  # Not unlimited
        current_count = Strategy.query.filter_by(user_id=current_user_id).count()
        if current_count >= max_strategies:
            return jsonify({'error': f'Maximum strategies limit reached for {user.subscription_tier} tier'}), 403
    
    # Create strategy
    strategy = Strategy(
        user_id=current_user_id,
        name=data['name'],
        type=data['type'],
        parameters=data['parameters']
    )
    
    db.session.add(strategy)
    db.session.commit()
    
    return jsonify({
        'message': 'Strategy created successfully',
        'strategy': strategy.to_dict()
    }), 201

@strategies_bp.route('/<int:strategy_id>', methods=['PUT'])
@jwt_required()
def update_strategy(strategy_id):
    """Update a strategy"""
    current_user_id = get_jwt_identity()
    strategy = Strategy.query.filter_by(id=strategy_id, user_id=current_user_id).first()
    
    if not strategy:
        return jsonify({'error': 'Strategy not found'}), 404
    
    data = request.get_json()
    
    # Update fields
    if 'name' in data:
        strategy.name = data['name']
    if 'type' in data:
        strategy.type = data['type']
    if 'parameters' in data:
        strategy.parameters = data['parameters']
    if 'is_active' in data:
        strategy.is_active = data['is_active']
    
    strategy.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Strategy updated successfully',
        'strategy': strategy.to_dict()
    }), 200

@strategies_bp.route('/<int:strategy_id>', methods=['DELETE'])
@jwt_required()
def delete_strategy(strategy_id):
    """Delete a strategy"""
    current_user_id = get_jwt_identity()
    strategy = Strategy.query.filter_by(id=strategy_id, user_id=current_user_id).first()
    
    if not strategy:
        return jsonify({'error': 'Strategy not found'}), 404
    
    db.session.delete(strategy)
    db.session.commit()
    
    return jsonify({'message': 'Strategy deleted successfully'}), 200

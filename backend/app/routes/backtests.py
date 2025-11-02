"""
Backtest Routes for Algorithmic Trading Platform
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Backtest, Strategy, User
from ..services.backtest_service import BacktestService
from datetime import datetime

backtests_bp = Blueprint('backtests', __name__, url_prefix='/api/backtests')

@backtests_bp.route('', methods=['GET'])
@jwt_required()
def get_backtests():
    """Get all backtests for current user"""
    current_user_id = get_jwt_identity()
    backtests = Backtest.query.filter_by(user_id=current_user_id).order_by(Backtest.created_at.desc()).all()
    
    return jsonify([backtest.to_dict() for backtest in backtests]), 200

@backtests_bp.route('/<int:backtest_id>', methods=['GET'])
@jwt_required()
def get_backtest(backtest_id):
    """Get a specific backtest"""
    current_user_id = get_jwt_identity()
    backtest = Backtest.query.filter_by(id=backtest_id, user_id=current_user_id).first()
    
    if not backtest:
        return jsonify({'error': 'Backtest not found'}), 404
    
    return jsonify(backtest.to_dict()), 200

@backtests_bp.route('', methods=['POST'])
@jwt_required()
def run_backtest():
    """Run a new backtest"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('strategy_id') or not data.get('symbol') or not data.get('start_date') or not data.get('end_date'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if strategy exists and belongs to user
    strategy = Strategy.query.filter_by(id=data['strategy_id'], user_id=current_user_id).first()
    if not strategy:
        return jsonify({'error': 'Strategy not found'}), 404
    
    # Check subscription limits
    from backend.config import config
    tier_config = config['default'].SUBSCRIPTION_TIERS.get(user.subscription_tier, {})
    max_backtests = tier_config.get('max_backtests_per_day', 5)
    
    if max_backtests != -1:  # Not unlimited
        from datetime import timedelta
        today = datetime.utcnow().date()
        today_start = datetime.combine(today, datetime.min.time())
        today_backtests = Backtest.query.filter(
            Backtest.user_id == current_user_id,
            Backtest.created_at >= today_start
        ).count()
        
        if today_backtests >= max_backtests:
            return jsonify({'error': f'Daily backtest limit reached for {user.subscription_tier} tier'}), 403
    
    try:
        # Run backtest
        backtest_service = BacktestService()
        performance, outperformance, results_data = backtest_service.run_backtest(
            strategy_type=strategy.type,
            parameters=strategy.parameters,
            symbol=data['symbol'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            transaction_cost=data.get('transaction_cost', 0.0001)
        )
        
        # Save backtest results
        backtest = Backtest(
            user_id=current_user_id,
            strategy_id=strategy.id,
            symbol=data['symbol'],
            start_date=datetime.fromisoformat(data['start_date']),
            end_date=datetime.fromisoformat(data['end_date']),
            performance=performance,
            outperformance=outperformance,
            results_data=results_data
        )
        
        db.session.add(backtest)
        db.session.commit()
        
        return jsonify({
            'message': 'Backtest completed successfully',
            'backtest': backtest.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Backtest failed: {str(e)}'}), 500

@backtests_bp.route('/<int:backtest_id>', methods=['DELETE'])
@jwt_required()
def delete_backtest(backtest_id):
    """Delete a backtest"""
    current_user_id = get_jwt_identity()
    backtest = Backtest.query.filter_by(id=backtest_id, user_id=current_user_id).first()
    
    if not backtest:
        return jsonify({'error': 'Backtest not found'}), 404
    
    db.session.delete(backtest)
    db.session.commit()
    
    return jsonify({'message': 'Backtest deleted successfully'}), 200

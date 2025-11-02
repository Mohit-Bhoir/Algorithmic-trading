"""
Subscription Routes for Algorithmic Trading Platform
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, User
from datetime import datetime, timedelta
import stripe

subscriptions_bp = Blueprint('subscriptions', __name__, url_prefix='/api/subscriptions')

@subscriptions_bp.route('/tiers', methods=['GET'])
def get_subscription_tiers():
    """Get available subscription tiers"""
    from backend.config import config
    tiers = config['default'].SUBSCRIPTION_TIERS
    return jsonify(tiers), 200

@subscriptions_bp.route('/current', methods=['GET'])
@jwt_required()
def get_current_subscription():
    """Get current user's subscription"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    from backend.config import config
    tier_config = config['default'].SUBSCRIPTION_TIERS.get(user.subscription_tier, {})
    
    return jsonify({
        'tier': user.subscription_tier,
        'tier_config': tier_config,
        'start_date': user.subscription_start_date.isoformat() if user.subscription_start_date else None,
        'end_date': user.subscription_end_date.isoformat() if user.subscription_end_date else None,
        'stripe_subscription_id': user.stripe_subscription_id
    }), 200

@subscriptions_bp.route('/checkout', methods=['POST'])
@jwt_required()
def create_checkout_session():
    """Create a Stripe checkout session for subscription"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    data = request.get_json()
    
    if not data or not data.get('tier'):
        return jsonify({'error': 'Missing tier'}), 400
    
    tier = data['tier']
    from backend.config import config
    tier_config = config['default'].SUBSCRIPTION_TIERS.get(tier)
    
    if not tier_config or tier == 'free':
        return jsonify({'error': 'Invalid subscription tier'}), 400
    
    try:
        # Initialize Stripe
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
        
        # Create or retrieve customer
        if not user.stripe_customer_id:
            customer = stripe.Customer.create(
                email=user.email,
                metadata={'user_id': user.id}
            )
            user.stripe_customer_id = customer.id
            db.session.commit()
        
        # Create checkout session
        checkout_session = stripe.checkout.Session.create(
            customer=user.stripe_customer_id,
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f'{tier_config["name"]} Subscription',
                        'description': f'Monthly subscription for {tier_config["name"]} tier'
                    },
                    'unit_amount': int(tier_config['price'] * 100),  # Convert to cents
                    'recurring': {
                        'interval': 'month'
                    }
                },
                'quantity': 1,
            }],
            mode='subscription',
            success_url=f'{current_app.config["FRONTEND_URL"]}/subscription/success?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'{current_app.config["FRONTEND_URL"]}/subscription/cancel',
            metadata={
                'user_id': user.id,
                'tier': tier
            }
        )
        
        return jsonify({
            'checkout_url': checkout_session.url,
            'session_id': checkout_session.id
        }), 200
        
    except Exception as e:
        # Log the actual error for debugging
        import logging
        logging.error(f'Failed to create checkout for user {user.id}: {str(e)}')
        return jsonify({'error': 'Failed to create checkout session. Please try again later.'}), 500

@subscriptions_bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events"""
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, current_app.config['STRIPE_WEBHOOK_SECRET']
        )
    except ValueError:
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError:
        return jsonify({'error': 'Invalid signature'}), 400
    
    # Handle different event types
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = int(session['metadata']['user_id'])
        tier = session['metadata']['tier']
        
        user = User.query.get(user_id)
        if user:
            user.subscription_tier = tier
            user.subscription_start_date = datetime.utcnow()
            user.subscription_end_date = datetime.utcnow() + timedelta(days=30)
            user.stripe_subscription_id = session.get('subscription')
            db.session.commit()
    
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        user = User.query.filter_by(stripe_subscription_id=subscription['id']).first()
        if user:
            user.subscription_tier = 'free'
            user.subscription_end_date = datetime.utcnow()
            db.session.commit()
    
    return jsonify({'status': 'success'}), 200

@subscriptions_bp.route('/cancel', methods=['POST'])
@jwt_required()
def cancel_subscription():
    """Cancel user's subscription"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.stripe_subscription_id:
        return jsonify({'error': 'No active subscription found'}), 404
    
    try:
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
        stripe.Subscription.delete(user.stripe_subscription_id)
        
        user.subscription_tier = 'free'
        user.subscription_end_date = datetime.utcnow()
        user.stripe_subscription_id = None
        db.session.commit()
        
        return jsonify({'message': 'Subscription cancelled successfully'}), 200
        
    except Exception as e:
        # Log the actual error for debugging
        import logging
        logging.error(f'Failed to cancel subscription for user {user.id}: {str(e)}')
        return jsonify({'error': 'Failed to cancel subscription. Please contact support.'}), 500

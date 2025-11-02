# Algorithmic Trading Platform - Full-Stack Web Application

This is a professional algorithmic trading platform that has been transformed from a command-line application into a full-stack web application with subscription-based access.

## Features

### For Traders
- **User Authentication**: Secure registration and login system
- **Multiple Trading Strategies**: Support for SMA, Mean Reversion, and ML-based strategies
- **Backtesting**: Test strategies against historical data
- **Live Trading**: Execute trades with multiple broker integrations (OANDA, IBKR, FXCM)
- **Performance Analytics**: Track and visualize trading performance
- **Subscription Plans**: Tiered access with different feature limits

### Technology Stack
- **Backend**: Flask (Python), PostgreSQL, JWT Authentication
- **Frontend**: React, Material-UI, Recharts
- **Payment**: Stripe integration for subscriptions
- **Deployment**: Docker, Docker Compose

## Subscription Tiers

### Free Tier
- 1 strategy
- 5 backtests per day
- No live trading
- $0/month

### Basic Tier
- 5 strategies
- 50 backtests per day
- Live trading enabled
- $29.99/month

### Professional Tier
- 20 strategies
- 200 backtests per day
- Live trading enabled
- Priority support
- $99.99/month

### Enterprise Tier
- Unlimited strategies
- Unlimited backtests
- Live trading enabled
- Dedicated support
- Custom integration
- $299.99/month

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.12+ (for local development)

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/Mohit-Bhoir/Algorithmic-trading.git
cd Algorithmic-trading
```

2. Copy the environment file and configure:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the application:
```bash
docker-compose up -d
```

4. Access the application:
- Frontend: http://localhost
- Backend API: http://localhost:5000
- API Documentation: http://localhost:5000/api/docs

### Local Development

#### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export FLASK_ENV=development
export DATABASE_URL=sqlite:///trading.db
```

4. Run the backend:
```bash
cd backend
python run.py
```

#### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Set up environment:
```bash
echo "REACT_APP_API_URL=http://localhost:5000/api" > .env
```

3. Run the frontend:
```bash
npm start
```

## API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - Logout user

### Strategy Endpoints
- `GET /api/strategies` - Get all user strategies
- `GET /api/strategies/<id>` - Get specific strategy
- `POST /api/strategies` - Create new strategy
- `PUT /api/strategies/<id>` - Update strategy
- `DELETE /api/strategies/<id>` - Delete strategy

### Backtest Endpoints
- `GET /api/backtests` - Get all user backtests
- `GET /api/backtests/<id>` - Get specific backtest
- `POST /api/backtests` - Run new backtest
- `DELETE /api/backtests/<id>` - Delete backtest

### Subscription Endpoints
- `GET /api/subscriptions/tiers` - Get available tiers
- `GET /api/subscriptions/current` - Get current subscription
- `POST /api/subscriptions/checkout` - Create checkout session
- `POST /api/subscriptions/cancel` - Cancel subscription
- `POST /api/subscriptions/webhook` - Stripe webhook handler

## Broker Integration

### OANDA
Configure your OANDA credentials in the application settings. You'll need:
- API Token
- Account ID
- Practice/Live account selection

### Interactive Brokers (IBKR)
Set up TWS or IB Gateway and configure:
- Host and port
- Client ID
- Account ID

### FXCM
Configure FXCM API credentials:
- API Token
- Account ID
- Server URL

## Security

- All passwords are hashed using bcrypt
- JWT tokens for authentication
- API rate limiting
- CORS protection
- SQL injection prevention via ORM
- XSS protection

## Deployment

### Production Deployment

1. Update environment variables in `.env`:
```bash
FLASK_ENV=production
SECRET_KEY=<your-strong-secret-key>
JWT_SECRET_KEY=<your-jwt-secret-key>
STRIPE_SECRET_KEY=<your-stripe-secret-key>
```

2. Use PostgreSQL instead of SQLite:
```bash
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

3. Deploy using Docker Compose:
```bash
docker-compose -f docker-compose.yml up -d
```

### Cloud Deployment Options
- **AWS**: Use ECS/EKS for containers, RDS for database
- **Google Cloud**: Use Cloud Run, Cloud SQL
- **Azure**: Use Azure Container Instances, Azure Database
- **Heroku**: Use Heroku containers with Postgres add-on

## Testing

Run backend tests:
```bash
cd backend
pytest
```

Run frontend tests:
```bash
cd frontend
npm test
```

## Contributing

This is a commercial product. For contribution inquiries, please contact the repository owner.

## License

Proprietary - All rights reserved

## Support

For support and inquiries:
- Email: support@algotrading.com
- Documentation: https://docs.algotrading.com

## Disclaimer

Trading financial instruments carries a high level of risk. This software is provided for educational and research purposes. Use at your own risk. Always test strategies thoroughly before live trading.

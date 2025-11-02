# Deployment Guide - Algorithmic Trading Platform

This guide covers deploying the Algorithmic Trading Platform to production.

## Table of Contents
1. [Pre-requisites](#pre-requisites)
2. [Environment Configuration](#environment-configuration)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Database Setup](#database-setup)
6. [Stripe Configuration](#stripe-configuration)
7. [Security Considerations](#security-considerations)
8. [Monitoring and Maintenance](#monitoring-and-maintenance)

## Pre-requisites

### Required
- Docker and Docker Compose (for containerized deployment)
- PostgreSQL 15+
- Node.js 18+ (for local development)
- Python 3.12+
- Domain name (for production)
- SSL certificate (Let's Encrypt recommended)

### Recommended
- nginx or Caddy for reverse proxy
- Redis for session management (future enhancement)
- Monitoring tools (Prometheus, Grafana)

## Environment Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Update the following critical variables:

### Security Keys (REQUIRED - Generate strong random keys)
```bash
# Generate SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate JWT_SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Database Configuration
```env
DATABASE_URL=postgresql://username:password@hostname:5432/dbname
```

### Stripe Configuration (for payments)
```env
STRIPE_PUBLIC_KEY=pk_live_your_live_key
STRIPE_SECRET_KEY=sk_live_your_live_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

### CORS Configuration
```env
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## Docker Deployment

### Local Development
```bash
docker-compose up -d
```

### Production Deployment

1. Update docker-compose.yml for production:
```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups

  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    restart: always
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - SECRET_KEY=${SECRET_KEY}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    depends_on:
      - db

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    restart: always
    depends_on:
      - backend

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx-prod.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - backend
      - frontend
```

2. Build and start:
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

## Cloud Deployment

### AWS Deployment

#### Using ECS (Elastic Container Service)

1. **Create ECR repositories:**
```bash
aws ecr create-repository --repository-name algo-trading-backend
aws ecr create-repository --repository-name algo-trading-frontend
```

2. **Push images to ECR:**
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker build -f Dockerfile.backend -t algo-trading-backend .
docker tag algo-trading-backend:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/algo-trading-backend:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/algo-trading-backend:latest
```

3. **Create RDS PostgreSQL instance:**
```bash
aws rds create-db-instance \
    --db-instance-identifier algo-trading-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username admin \
    --master-user-password YOUR_PASSWORD \
    --allocated-storage 20
```

4. **Create ECS Task Definition and Service** (see AWS documentation)

### Heroku Deployment

1. **Install Heroku CLI and login:**
```bash
heroku login
```

2. **Create Heroku app:**
```bash
heroku create algo-trading-platform
```

3. **Add PostgreSQL:**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. **Set environment variables:**
```bash
heroku config:set SECRET_KEY=your_secret_key
heroku config:set JWT_SECRET_KEY=your_jwt_secret
heroku config:set STRIPE_SECRET_KEY=your_stripe_key
```

5. **Deploy:**
```bash
git push heroku main
```

### DigitalOcean App Platform

1. Connect your GitHub repository
2. Configure build settings:
   - Backend: Python, run command: `gunicorn backend.run:app`
   - Frontend: Node.js, build: `npm run build`, output: `build/`
3. Add PostgreSQL database from marketplace
4. Set environment variables in the dashboard
5. Deploy

## Database Setup

### Initial Migration
```bash
# Create database tables
docker-compose exec backend python3 -c "from backend.app import create_app; app = create_app(); app.app_context().push(); from backend.app.models import db; db.create_all()"
```

### Database Backups
```bash
# Backup
docker-compose exec db pg_dump -U trading_user trading_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore
docker-compose exec -T db psql -U trading_user trading_db < backup.sql
```

### Automated Backups (add to crontab)
```bash
0 2 * * * cd /path/to/app && docker-compose exec db pg_dump -U trading_user trading_db > /backups/backup_$(date +\%Y\%m\%d).sql
```

## Stripe Configuration

1. **Create Stripe account** at https://stripe.com

2. **Get API keys** from Stripe Dashboard

3. **Configure webhook endpoint:**
   - URL: `https://yourdomain.com/api/subscriptions/webhook`
   - Events to listen for:
     - `checkout.session.completed`
     - `customer.subscription.deleted`
     - `customer.subscription.updated`

4. **Test webhook locally** using Stripe CLI:
```bash
stripe listen --forward-to localhost:5000/api/subscriptions/webhook
```

## Security Considerations

### SSL/TLS
- Use Let's Encrypt for free SSL certificates
- Configure HTTPS-only in production
- Set up automatic certificate renewal

### API Security
- Enable rate limiting (implement Flask-Limiter)
- Use CORS properly (restrict origins)
- Implement request validation
- Use prepared statements (SQLAlchemy ORM)

### Secrets Management
- Never commit secrets to git
- Use environment variables
- Consider using AWS Secrets Manager or HashiCorp Vault
- Rotate keys regularly

### Database Security
- Use strong passwords
- Enable SSL for database connections
- Restrict database access by IP
- Regular backups
- Enable query logging for auditing

### Authentication
- JWT tokens with short expiration
- Secure password hashing (bcrypt)
- Implement rate limiting on auth endpoints
- Consider 2FA for premium accounts

## Monitoring and Maintenance

### Health Checks
```bash
# Check API health
curl https://yourdomain.com/health

# Check database connection
docker-compose exec backend python3 -c "from backend.app import create_app; app = create_app(); app.app_context().push(); from backend.app.models import db; db.engine.connect(); print('DB OK')"
```

### Logging
- Configure centralized logging (ELK stack, CloudWatch)
- Monitor error rates
- Track API response times
- Log authentication attempts

### Performance Monitoring
- Set up APM (Application Performance Monitoring)
- Monitor database query performance
- Track API endpoint latency
- Monitor container resource usage

### Regular Maintenance
- Update dependencies monthly
- Security patches immediately
- Database optimization quarterly
- Review and rotate logs weekly
- Test backups monthly

## Scaling Considerations

### Horizontal Scaling
- Use load balancer (AWS ALB, nginx)
- Run multiple backend instances
- Implement session store (Redis)
- Use CDN for frontend assets

### Database Scaling
- Read replicas for reporting
- Connection pooling
- Query optimization
- Consider sharding for large datasets

### Caching
- Redis for session management
- Cache frequently accessed data
- CDN for static assets
- API response caching

## Troubleshooting

### Backend won't start
- Check environment variables
- Verify database connection
- Check logs: `docker-compose logs backend`
- Ensure all dependencies are installed

### Database connection errors
- Verify DATABASE_URL
- Check database is running
- Verify firewall rules
- Test connection manually

### Frontend can't reach backend
- Check CORS settings
- Verify API URL configuration
- Check network connectivity
- Review nginx/proxy configuration

## Support and Resources

- Documentation: https://docs.algotrading.com
- GitHub Issues: https://github.com/Mohit-Bhoir/Algorithmic-trading/issues
- Email: support@algotrading.com

## License
Proprietary - All rights reserved

# Architecture Overview

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                    (React Frontend App)                          │
│                                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │  Login/  │  │Dashboard │  │Strategies│  │Subscribe │       │
│  │ Register │  │          │  │          │  │          │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                                                                   │
│              ▼ HTTP/HTTPS (JWT Token Auth) ▼                    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ REST API Calls
                                │
┌─────────────────────────────────────────────────────────────────┐
│                      NGINX (Reverse Proxy)                       │
│                   - SSL/TLS Termination                          │
│                   - Load Balancing                               │
│                   - Static File Serving                          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FLASK BACKEND API (Python)                     │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Authentication Layer (JWT)                              │   │
│  │  - Login, Register, Token Refresh                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Strategies  │  │  Backtests   │  │Subscriptions │         │
│  │  Routes      │  │  Routes      │  │  Routes      │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│         │                  │                  │                  │
│         ▼                  ▼                  ▼                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         Business Logic & Services                        │  │
│  │  - Strategy Management                                   │  │
│  │  - Backtest Execution (SMA, Mean Reversion)             │  │
│  │  - Subscription Tier Enforcement                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                    │                        │
                    │                        │
                    ▼                        ▼
┌──────────────────────────┐   ┌────────────────────────┐
│   PostgreSQL Database     │   │   Stripe Payment API   │
│                           │   │                        │
│  ┌────────────────────┐  │   │  - Checkout Sessions  │
│  │ Users              │  │   │  - Subscriptions      │
│  │ Strategies         │  │   │  - Webhooks           │
│  │ Backtests          │  │   └────────────────────────┘
│  │ Trading Sessions   │  │
│  │ Broker Credentials │  │
│  │ Subscription Data  │  │
│  └────────────────────┘  │
└──────────────────────────┘
```

## Data Flow Examples

### 1. User Registration
```
User → Frontend → POST /api/auth/register → Backend
                                           ↓
                                    Hash Password (bcrypt)
                                           ↓
                                    Create User Record
                                           ↓
                                      Save to DB
                                           ↓
                                  Generate JWT Tokens
                                           ↓
                          Return tokens + user data → Frontend
                                                           ↓
                                                  Store in localStorage
```

### 2. Creating a Strategy
```
User → Frontend → POST /api/strategies (with JWT) → Backend
                                                    ↓
                                            Verify JWT Token
                                                    ↓
                                        Check Subscription Limits
                                                    ↓
                                            Create Strategy
                                                    ↓
                                            Save to Database
                                                    ↓
                                    Return strategy data → Frontend
```

### 3. Running a Backtest
```
User → Frontend → POST /api/backtests → Backend
                                        ↓
                                Verify JWT & Limits
                                        ↓
                            Load Historical Data (Part5_Materials)
                                        ↓
                            Execute Strategy (SMA/MeanRev)
                                        ↓
                            Calculate Performance Metrics
                                        ↓
                            Save Results to Database
                                        ↓
                        Return performance data → Frontend
                                                        ↓
                                            Display Charts & Stats
```

### 4. Subscription Upgrade
```
User → Frontend → POST /api/subscriptions/checkout → Backend
                                                     ↓
                                            Create Stripe Customer
                                                     ↓
                                        Create Checkout Session
                                                     ↓
                                    Redirect to Stripe → User Pays
                                                                 ↓
                                                    Stripe Webhook
                                                                 ↓
                                            Backend Updates Subscription
                                                                 ↓
                                                User Redirected Back
```

## Technology Stack Details

### Frontend
- **React 18**: Modern UI framework
- **Material-UI 5**: Component library
- **Axios**: HTTP client
- **React Router**: Navigation
- **Recharts**: Data visualization (for future charts)

### Backend
- **Flask 3**: Web framework
- **SQLAlchemy**: ORM
- **Flask-JWT-Extended**: Authentication
- **Flask-CORS**: Cross-origin support
- **Bcrypt**: Password hashing
- **Stripe**: Payment processing

### Database
- **PostgreSQL 15**: Production database
- **SQLite**: Development/testing

### Deployment
- **Docker**: Containerization
- **Docker Compose**: Orchestration
- **Nginx**: Reverse proxy
- **Gunicorn**: WSGI server

## Security Layers

```
┌──────────────────────────────────────────┐
│ 1. HTTPS/TLS (Transport Encryption)     │
└──────────────────────────────────────────┘
                  ↓
┌──────────────────────────────────────────┐
│ 2. CORS (Origin Validation)              │
└──────────────────────────────────────────┘
                  ↓
┌──────────────────────────────────────────┐
│ 3. JWT Authentication (Access Control)   │
└──────────────────────────────────────────┘
                  ↓
┌──────────────────────────────────────────┐
│ 4. Input Validation                      │
└──────────────────────────────────────────┘
                  ↓
┌──────────────────────────────────────────┐
│ 5. SQL Injection Prevention (ORM)        │
└──────────────────────────────────────────┘
                  ↓
┌──────────────────────────────────────────┐
│ 6. Password Hashing (bcrypt)             │
└──────────────────────────────────────────┘
                  ↓
┌──────────────────────────────────────────┐
│ 7. No Stack Trace Exposure               │
└──────────────────────────────────────────┘
```

## Subscription Tier Enforcement

```
API Request
    ↓
Get User Subscription Tier
    ↓
Check Tier Limits
    ├─→ Free: 1 strategy, 5 backtests/day
    ├─→ Basic: 5 strategies, 50 backtests/day
    ├─→ Professional: 20 strategies, 200 backtests/day
    └─→ Enterprise: Unlimited
    ↓
Allow or Reject Request
```

## Deployment Architecture (Production)

```
                    ┌──────────────────┐
                    │   Domain Name    │
                    │  (your-site.com) │
                    └──────────────────┘
                            │
                            ▼
                    ┌──────────────────┐
                    │   SSL/TLS Cert   │
                    │  (Let's Encrypt) │
                    └──────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │      Load Balancer / CDN              │
        └───────────────────────────────────────┘
                            │
        ┌───────────────────┴───────────────────┐
        │                                       │
        ▼                                       ▼
┌──────────────────┐                  ┌──────────────────┐
│  Frontend Static │                  │  Backend API     │
│  Files (S3/CDN)  │                  │  (ECS/Heroku)    │
└──────────────────┘                  └──────────────────┘
                                              │
                            ┌─────────────────┴─────────────────┐
                            │                                   │
                            ▼                                   ▼
                    ┌──────────────┐                  ┌──────────────┐
                    │  PostgreSQL  │                  │    Stripe    │
                    │   Database   │                  │     API      │
                    │    (RDS)     │                  └──────────────┘
                    └──────────────┘
```

## Scalability Considerations

### Horizontal Scaling
- Multiple backend instances behind load balancer
- Stateless API design (JWT tokens)
- Database connection pooling
- Redis for session management (future)

### Performance Optimization
- Database indexing on foreign keys
- API response caching (future)
- CDN for static assets
- Lazy loading in frontend
- Pagination for list endpoints

### Monitoring
- Application logs
- Database query performance
- API response times
- Error tracking
- User analytics

This architecture is designed to handle growth from initial launch to thousands of concurrent users.

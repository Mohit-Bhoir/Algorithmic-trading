# User Guide - Algorithmic Trading Platform

Welcome to the Algorithmic Trading Platform! This guide will help you get started with creating, testing, and executing trading strategies.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Creating Your First Strategy](#creating-your-first-strategy)
3. [Running Backtests](#running-backtests)
4. [Understanding Strategy Types](#understanding-strategy-types)
5. [Subscription Plans](#subscription-plans)
6. [Live Trading](#live-trading)
7. [Best Practices](#best-practices)
8. [FAQ](#faq)

## Getting Started

### Creating an Account

1. Navigate to the registration page
2. Enter your username, email, and password
3. Click "Sign Up"
4. You'll be automatically logged in with a **Free** tier account

### Dashboard Overview

After logging in, you'll see your dashboard with:
- **Strategies**: Number of strategies you've created
- **Backtests**: Total backtests run
- **Active Sessions**: Currently running live trading sessions
- **Total P&L**: Your profit and loss from live trading

## Creating Your First Strategy

### Step-by-Step Guide

1. **Navigate to Strategies**
   - Click "Strategies" in the navigation bar
   - Or click "Create Strategy" on the dashboard

2. **Click "Create Strategy"**

3. **Fill in Strategy Details**
   - **Name**: Give your strategy a descriptive name (e.g., "EURUSD SMA Crossover")
   - **Type**: Choose from available strategy types
   - **Parameters**: Configure strategy-specific parameters

4. **Click "Create"**

Your strategy is now saved and ready to backtest!

## Running Backtests

Backtesting allows you to test your strategy against historical data to see how it would have performed.

### How to Run a Backtest

1. Go to your Strategies page
2. Find the strategy you want to test
3. Click the "Backtest" button
4. Configure backtest parameters:
   - **Symbol**: Trading pair (e.g., EUR_USD)
   - **Start Date**: Beginning of test period
   - **End Date**: End of test period
   - **Transaction Cost**: Cost per trade (default: 0.01%)

5. Click "Run Backtest"

### Understanding Backtest Results

After running a backtest, you'll see:
- **Performance**: Total return of the strategy
- **Outperformance**: Strategy return vs. buy-and-hold
- **Chart**: Visual comparison of strategy vs. buy-and-hold
- **Statistics**: Win rate, max drawdown, Sharpe ratio

### Backtest Limits by Plan
- **Free**: 5 backtests per day
- **Basic**: 50 backtests per day
- **Professional**: 200 backtests per day
- **Enterprise**: Unlimited

## Understanding Strategy Types

### 1. Simple Moving Average (SMA) Crossover

**How it works:**
- Uses two moving averages: short-term and long-term
- **Buy Signal**: Short MA crosses above long MA
- **Sell Signal**: Short MA crosses below long MA

**Parameters:**
- `SMA_S`: Short moving average period (default: 10)
- `SMA_L`: Long moving average period (default: 50)

**Best for:**
- Trending markets
- Medium to long-term trading
- Liquid instruments

**Example Configuration:**
```
Name: EUR/USD SMA Strategy
Type: SMA
SMA_S: 20
SMA_L: 50
```

### 2. Mean Reversion

**How it works:**
- Assumes price will revert to its average
- **Buy Signal**: Price falls below lower band
- **Sell Signal**: Price rises above upper band
- **Exit**: Price crosses the moving average

**Parameters:**
- `SMA`: Moving average period (default: 20)
- `dev`: Standard deviation multiplier (default: 2)

**Best for:**
- Range-bound markets
- High-volatility instruments
- Short to medium-term trading

**Example Configuration:**
```
Name: Mean Reversion Bitcoin
Type: MeanReversion
SMA: 25
dev: 2.5
```

## Subscription Plans

### Free Tier
- **Cost**: $0/month
- **Features**:
  - 1 strategy
  - 5 backtests per day
  - No live trading
  - Community support

### Basic Tier
- **Cost**: $29.99/month
- **Features**:
  - 5 strategies
  - 50 backtests per day
  - Live trading enabled
  - Email support
  - All strategy types

### Professional Tier
- **Cost**: $99.99/month
- **Features**:
  - 20 strategies
  - 200 backtests per day
  - Live trading enabled
  - Priority support
  - Advanced analytics
  - API access

### Enterprise Tier
- **Cost**: $299.99/month
- **Features**:
  - Unlimited strategies
  - Unlimited backtests
  - Live trading enabled
  - Dedicated support
  - Custom integrations
  - White-label options

### How to Upgrade

1. Go to the "Subscription" page
2. Click "Upgrade" on your desired plan
3. You'll be redirected to Stripe checkout
4. Enter your payment details
5. Your subscription will activate immediately

## Live Trading

**⚠️ WARNING: Live trading involves real money and real risk. Only available on paid plans.**

### Connecting Your Broker

We support the following brokers:
- **OANDA**: Forex and CFDs
- **Interactive Brokers (IBKR)**: Stocks, forex, options
- **FXCM**: Forex and CFDs

### Setting Up Live Trading

1. **Configure Broker Credentials**
   - Go to Settings → Broker Connections
   - Select your broker
   - Enter API credentials
   - Choose Demo or Live account
   - Save credentials

2. **Start a Trading Session**
   - Go to Strategies
   - Select the strategy to trade
   - Click "Start Live Trading"
   - Configure:
     - Trading instrument
     - Position size
     - Stop loss (optional)
     - Take profit (optional)
   - Confirm and start

3. **Monitor Your Session**
   - View real-time positions
   - Track profit/loss
   - Review trade history
   - Stop trading anytime

### Risk Management

**Always use stop losses:**
- Protects against large losses
- Automatically closes losing positions
- Recommended: 1-2% of account per trade

**Position Sizing:**
- Never risk more than 2% per trade
- Use appropriate leverage
- Consider correlation between instruments

**Testing:**
- Test strategies thoroughly in backtests
- Use demo accounts before live trading
- Start with small position sizes

## Best Practices

### Strategy Development

1. **Start Simple**
   - Begin with basic strategies
   - Understand how they work
   - Add complexity gradually

2. **Use Historical Data**
   - Test on multiple time periods
   - Include different market conditions
   - Verify results across instruments

3. **Avoid Overfitting**
   - Don't optimize too much
   - Use out-of-sample testing
   - Keep strategies simple

### Risk Management

1. **Diversification**
   - Use multiple strategies
   - Trade different instruments
   - Vary timeframes

2. **Position Sizing**
   - Risk only 1-2% per trade
   - Adjust for volatility
   - Scale in/out gradually

3. **Monitoring**
   - Check positions daily
   - Review performance weekly
   - Adjust strategies as needed

### Performance Tracking

1. **Keep a Trading Journal**
   - Record all trades
   - Note market conditions
   - Document lessons learned

2. **Analyze Results**
   - Review win/loss ratio
   - Calculate risk-reward
   - Identify improvement areas

3. **Continuous Improvement**
   - Learn from mistakes
   - Stay updated on markets
   - Adapt to changing conditions

## FAQ

### How do I reset my password?
Click "Forgot Password" on the login page and follow the instructions.

### Can I use multiple strategies simultaneously?
Yes, depending on your subscription plan's strategy limit.

### What happens if I exceed my backtest limit?
You'll need to wait until the next day or upgrade to a higher tier.

### Can I cancel my subscription anytime?
Yes, you can cancel anytime. Your access continues until the end of your billing period.

### Is my broker API key secure?
Yes, all credentials are encrypted and stored securely. We never share your credentials.

### What instruments can I trade?
This depends on your broker. Most support forex, some support stocks, CFDs, and options.

### Do you provide trading signals?
No, this is a platform for running YOUR strategies. We don't provide trading advice.

### Can I export my data?
Yes, you can export backtest results and trading history from your account.

### What are transaction costs?
These are fees charged by brokers per trade. Include them in backtests for accuracy.

### How accurate are backtests?
Backtests are based on historical data and may not reflect future performance. Past performance does not guarantee future results.

## Support

### Getting Help

- **Documentation**: https://docs.algotrading.com
- **Email Support**: support@algotrading.com
- **Community Forum**: https://community.algotrading.com

### Response Times
- **Free tier**: 48 hours
- **Basic tier**: 24 hours
- **Professional tier**: 12 hours
- **Enterprise tier**: 4 hours

## Disclaimer

Trading financial instruments carries a high level of risk and may not be suitable for all investors. The high degree of leverage can work against you as well as for you. Before deciding to trade, you should carefully consider your investment objectives, level of experience, and risk appetite. 

This platform is provided for educational and research purposes. Past performance is not indicative of future results. Always test strategies thoroughly before live trading.

## License

Proprietary - All rights reserved

---

**Happy Trading! 📈**

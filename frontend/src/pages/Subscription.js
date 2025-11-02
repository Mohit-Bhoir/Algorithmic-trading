import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Button,
  Box,
  Card,
  CardContent,
  CardActions,
  Chip,
} from '@mui/material';
import { CheckCircle, Upgrade } from '@mui/icons-material';
import { subscriptionsAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

function Subscription() {
  const { user } = useAuth();
  const [tiers, setTiers] = useState({});
  const [currentSubscription, setCurrentSubscription] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadSubscriptionData();
  }, []);

  const loadSubscriptionData = async () => {
    try {
      const [tiersRes, currentRes] = await Promise.all([
        subscriptionsAPI.getTiers(),
        subscriptionsAPI.getCurrent(),
      ]);
      setTiers(tiersRes.data);
      setCurrentSubscription(currentRes.data);
    } catch (error) {
      console.error('Failed to load subscription data:', error);
    }
  };

  const handleUpgrade = async (tier) => {
    if (tier === 'free') return;
    
    setLoading(true);
    try {
      const response = await subscriptionsAPI.createCheckout(tier);
      // Redirect to Stripe checkout
      window.location.href = response.data.checkout_url;
    } catch (error) {
      console.error('Failed to create checkout:', error);
      alert('Failed to start checkout process. Please try again.');
    }
    setLoading(false);
  };

  const handleCancel = async () => {
    if (!window.confirm('Are you sure you want to cancel your subscription?')) {
      return;
    }

    setLoading(true);
    try {
      await subscriptionsAPI.cancel();
      alert('Subscription cancelled successfully');
      loadSubscriptionData();
    } catch (error) {
      console.error('Failed to cancel subscription:', error);
      alert('Failed to cancel subscription. Please try again.');
    }
    setLoading(false);
  };

  const tierOrder = ['free', 'basic', 'professional', 'enterprise'];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Subscription Plans
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Current Plan: <strong>{currentSubscription?.tier || 'Free'}</strong>
      </Typography>

      <Grid container spacing={3}>
        {tierOrder.map((tierKey) => {
          const tier = tiers[tierKey];
          if (!tier) return null;

          const isCurrentTier = currentSubscription?.tier === tierKey;
          const isFree = tierKey === 'free';

          return (
            <Grid item xs={12} md={6} lg={3} key={tierKey}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  position: 'relative',
                  border: isCurrentTier ? '2px solid' : '1px solid',
                  borderColor: isCurrentTier ? 'primary.main' : 'divider',
                }}
              >
                {isCurrentTier && (
                  <Chip
                    label="Current Plan"
                    color="primary"
                    size="small"
                    sx={{ position: 'absolute', top: 16, right: 16 }}
                  />
                )}
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography variant="h5" gutterBottom>
                    {tier.name}
                  </Typography>
                  <Typography variant="h4" color="primary" gutterBottom>
                    ${tier.price}
                    <Typography variant="body2" component="span" color="text.secondary">
                      /month
                    </Typography>
                  </Typography>
                  
                  <Box sx={{ mt: 3 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <CheckCircle color="success" sx={{ mr: 1, fontSize: 20 }} />
                      <Typography variant="body2">
                        {tier.max_strategies === -1
                          ? 'Unlimited strategies'
                          : `${tier.max_strategies} ${tier.max_strategies === 1 ? 'strategy' : 'strategies'}`}
                      </Typography>
                    </Box>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <CheckCircle color="success" sx={{ mr: 1, fontSize: 20 }} />
                      <Typography variant="body2">
                        {tier.max_backtests_per_day === -1
                          ? 'Unlimited backtests'
                          : `${tier.max_backtests_per_day} backtests/day`}
                      </Typography>
                    </Box>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <CheckCircle
                        color={tier.live_trading ? 'success' : 'disabled'}
                        sx={{ mr: 1, fontSize: 20 }}
                      />
                      <Typography variant="body2" color={tier.live_trading ? 'inherit' : 'text.secondary'}>
                        {tier.live_trading ? 'Live trading' : 'No live trading'}
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>
                <CardActions sx={{ p: 2, pt: 0 }}>
                  {isFree ? (
                    <Button fullWidth variant="outlined" disabled>
                      Free Forever
                    </Button>
                  ) : isCurrentTier ? (
                    <Button
                      fullWidth
                      variant="outlined"
                      color="error"
                      onClick={handleCancel}
                      disabled={loading}
                    >
                      Cancel Subscription
                    </Button>
                  ) : (
                    <Button
                      fullWidth
                      variant="contained"
                      startIcon={<Upgrade />}
                      onClick={() => handleUpgrade(tierKey)}
                      disabled={loading}
                    >
                      Upgrade
                    </Button>
                  )}
                </CardActions>
              </Card>
            </Grid>
          );
        })}
      </Grid>

      <Paper sx={{ mt: 4, p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Frequently Asked Questions
        </Typography>
        <Box sx={{ mt: 2 }}>
          <Typography variant="subtitle2" gutterBottom>
            Can I cancel anytime?
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            Yes, you can cancel your subscription at any time. Your access will continue until the end of your billing period.
          </Typography>

          <Typography variant="subtitle2" gutterBottom>
            How do payments work?
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            All payments are processed securely through Stripe. You'll be billed monthly on the date you subscribed.
          </Typography>

          <Typography variant="subtitle2" gutterBottom>
            What happens if I exceed my limits?
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            If you reach your strategy or backtest limits, you'll need to upgrade to a higher tier to continue using those features.
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
}

export default Subscription;

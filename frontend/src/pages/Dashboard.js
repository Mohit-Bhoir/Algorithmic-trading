import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
} from '@mui/material';
import {
  TrendingUp,
  AccountBalance,
  ShowChart,
  AutoGraph,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { strategiesAPI, backtestsAPI, subscriptionsAPI } from '../services/api';

function Dashboard() {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    strategies: 0,
    backtests: 0,
    activeSessions: 0,
  });
  const [subscription, setSubscription] = useState(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [strategiesRes, backtestsRes, subRes] = await Promise.all([
        strategiesAPI.getAll(),
        backtestsAPI.getAll(),
        subscriptionsAPI.getCurrent(),
      ]);

      setStats({
        strategies: strategiesRes.data.length,
        backtests: backtestsRes.data.length,
        activeSessions: 0, // TODO: implement active sessions tracking
      });

      setSubscription(subRes.data);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Welcome back, {user?.username}!
      </Typography>
      
      <Box sx={{ mb: 3 }}>
        <Typography variant="body1" color="text.secondary">
          Current Plan: <strong>{subscription?.tier || 'Free'}</strong>
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Statistics Cards */}
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <ShowChart color="primary" sx={{ fontSize: 40, mr: 2 }} />
                <Box>
                  <Typography variant="h4">{stats.strategies}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Strategies
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <AutoGraph color="success" sx={{ fontSize: 40, mr: 2 }} />
                <Box>
                  <Typography variant="h4">{stats.backtests}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Backtests
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <TrendingUp color="warning" sx={{ fontSize: 40, mr: 2 }} />
                <Box>
                  <Typography variant="h4">{stats.activeSessions}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Active Sessions
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <AccountBalance color="info" sx={{ fontSize: 40, mr: 2 }} />
                <Box>
                  <Typography variant="h4">$0</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total P&L
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Quick Actions
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mt: 2 }}>
              <Button variant="contained" href="/strategies">
                Create Strategy
              </Button>
              <Button variant="outlined" href="/backtests">
                Run Backtest
              </Button>
              <Button variant="outlined" href="/subscription">
                Upgrade Plan
              </Button>
            </Box>
          </Paper>
        </Grid>

        {/* Recent Activity */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Activity
            </Typography>
            <Typography variant="body2" color="text.secondary">
              No recent activity to display
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default Dashboard;

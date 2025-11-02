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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  IconButton,
} from '@mui/material';
import { Add, Edit, Delete, PlayArrow } from '@mui/icons-material';
import { strategiesAPI } from '../services/api';

function Strategies() {
  const [strategies, setStrategies] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingStrategy, setEditingStrategy] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    type: 'SMA',
    parameters: {},
  });

  useEffect(() => {
    loadStrategies();
  }, []);

  const loadStrategies = async () => {
    try {
      const response = await strategiesAPI.getAll();
      setStrategies(response.data);
    } catch (error) {
      console.error('Failed to load strategies:', error);
    }
  };

  const handleOpenDialog = (strategy = null) => {
    if (strategy) {
      setEditingStrategy(strategy);
      setFormData({
        name: strategy.name,
        type: strategy.type,
        parameters: strategy.parameters,
      });
    } else {
      setEditingStrategy(null);
      setFormData({ name: '', type: 'SMA', parameters: {} });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingStrategy(null);
  };

  const handleSubmit = async () => {
    try {
      // Set default parameters based on strategy type
      let parameters = formData.parameters;
      if (formData.type === 'SMA' && !parameters.SMA_S) {
        parameters = { SMA_S: 10, SMA_L: 50 };
      } else if (formData.type === 'MeanReversion' && !parameters.SMA) {
        parameters = { SMA: 20, dev: 2 };
      }

      if (editingStrategy) {
        await strategiesAPI.update(editingStrategy.id, {
          ...formData,
          parameters,
        });
      } else {
        await strategiesAPI.create({ ...formData, parameters });
      }
      
      loadStrategies();
      handleCloseDialog();
    } catch (error) {
      console.error('Failed to save strategy:', error);
      alert(error.response?.data?.error || 'Failed to save strategy');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this strategy?')) {
      try {
        await strategiesAPI.delete(id);
        loadStrategies();
      } catch (error) {
        console.error('Failed to delete strategy:', error);
      }
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">My Strategies</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpenDialog()}
        >
          Create Strategy
        </Button>
      </Box>

      <Grid container spacing={3}>
        {strategies.map((strategy) => (
          <Grid item xs={12} md={6} lg={4} key={strategy.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {strategy.name}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Type: {strategy.type}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Parameters: {JSON.stringify(strategy.parameters)}
                </Typography>
                <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                  Created: {new Date(strategy.created_at).toLocaleDateString()}
                </Typography>
              </CardContent>
              <CardActions>
                <IconButton
                  size="small"
                  color="primary"
                  onClick={() => handleOpenDialog(strategy)}
                >
                  <Edit />
                </IconButton>
                <IconButton
                  size="small"
                  color="error"
                  onClick={() => handleDelete(strategy.id)}
                >
                  <Delete />
                </IconButton>
                <Button size="small" startIcon={<PlayArrow />}>
                  Backtest
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      {strategies.length === 0 && (
        <Paper sx={{ p: 3, textAlign: 'center', mt: 3 }}>
          <Typography variant="body1" color="text.secondary">
            No strategies yet. Create your first strategy to get started!
          </Typography>
        </Paper>
      )}

      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingStrategy ? 'Edit Strategy' : 'Create Strategy'}
        </DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Strategy Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            margin="normal"
          />
          <TextField
            fullWidth
            select
            label="Strategy Type"
            value={formData.type}
            onChange={(e) => setFormData({ ...formData, type: e.target.value })}
            margin="normal"
          >
            <MenuItem value="SMA">Simple Moving Average (SMA)</MenuItem>
            <MenuItem value="MeanReversion">Mean Reversion</MenuItem>
          </TextField>
          
          {formData.type === 'SMA' && (
            <>
              <TextField
                fullWidth
                label="Short SMA Period"
                type="number"
                value={formData.parameters.SMA_S || 10}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    parameters: { ...formData.parameters, SMA_S: parseInt(e.target.value) },
                  })
                }
                margin="normal"
              />
              <TextField
                fullWidth
                label="Long SMA Period"
                type="number"
                value={formData.parameters.SMA_L || 50}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    parameters: { ...formData.parameters, SMA_L: parseInt(e.target.value) },
                  })
                }
                margin="normal"
              />
            </>
          )}
          
          {formData.type === 'MeanReversion' && (
            <>
              <TextField
                fullWidth
                label="SMA Period"
                type="number"
                value={formData.parameters.SMA || 20}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    parameters: { ...formData.parameters, SMA: parseInt(e.target.value) },
                  })
                }
                margin="normal"
              />
              <TextField
                fullWidth
                label="Standard Deviation"
                type="number"
                value={formData.parameters.dev || 2}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    parameters: { ...formData.parameters, dev: parseInt(e.target.value) },
                  })
                }
                margin="normal"
              />
            </>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained">
            {editingStrategy ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export default Strategies;

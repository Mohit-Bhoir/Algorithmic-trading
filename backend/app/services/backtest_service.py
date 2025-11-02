"""
Backtest Service for running trading strategy backtests
"""
import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

# Add the Part5_Materials directory to the path to import backtester classes
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..', 'Part5_Materials'))

class BacktestService:
    """Service for running backtests on trading strategies"""
    
    def run_backtest(self, strategy_type, parameters, symbol, start_date, end_date, transaction_cost=0.0001):
        """
        Run a backtest for a given strategy
        
        Args:
            strategy_type: Type of strategy ('SMA', 'MeanReversion', 'ML')
            parameters: Strategy parameters as dictionary
            symbol: Trading symbol
            start_date: Start date (ISO format string)
            end_date: End date (ISO format string)
            transaction_cost: Transaction cost as decimal
            
        Returns:
            tuple: (performance, outperformance, results_data)
        """
        
        if strategy_type == 'SMA':
            return self._run_sma_backtest(parameters, symbol, start_date, end_date, transaction_cost)
        elif strategy_type == 'MeanReversion':
            return self._run_mean_reversion_backtest(parameters, symbol, start_date, end_date, transaction_cost)
        else:
            raise ValueError(f'Unsupported strategy type: {strategy_type}')
    
    def _run_sma_backtest(self, parameters, symbol, start_date, end_date, transaction_cost):
        """Run SMA strategy backtest"""
        from SMABacktester import SMABacktester
        
        sma_s = parameters.get('SMA_S', 10)
        sma_l = parameters.get('SMA_L', 50)
        
        backtester = SMABacktester(
            symbol=symbol,
            SMA_S=sma_s,
            SMA_L=sma_l,
            start=start_date,
            end=end_date,
            tc=transaction_cost
        )
        
        performance, outperformance = backtester.test_strategy()
        
        # Extract results data
        results_data = None
        if backtester.results is not None:
            results_df = backtester.results[['creturns', 'cstrategy']].tail(100)
            results_data = {
                'dates': results_df.index.strftime('%Y-%m-%d %H:%M:%S').tolist(),
                'buy_and_hold': results_df['creturns'].tolist(),
                'strategy': results_df['cstrategy'].tolist()
            }
        
        return performance, outperformance, results_data
    
    def _run_mean_reversion_backtest(self, parameters, symbol, start_date, end_date, transaction_cost):
        """Run Mean Reversion strategy backtest"""
        from MeanRevBacktester import MeanRevBacktester
        
        sma = parameters.get('SMA', 20)
        dev = parameters.get('dev', 2)
        
        backtester = MeanRevBacktester(
            symbol=symbol,
            SMA=sma,
            dev=dev,
            start=start_date,
            end=end_date,
            tc=transaction_cost
        )
        
        performance, outperformance = backtester.test_strategy()
        
        # Extract results data
        results_data = None
        if backtester.results is not None:
            results_df = backtester.results[['creturns', 'cstrategy']].tail(100)
            results_data = {
                'dates': results_df.index.strftime('%Y-%m-%d %H:%M:%S').tolist(),
                'buy_and_hold': results_df['creturns'].tolist(),
                'strategy': results_df['cstrategy'].tolist()
            }
        
        return performance, outperformance, results_data

"""
Feature Engineering for NSE Stock Clustering

This module creates financial features from stock price data to identify risk patterns.
We calculate volatility, returns, technical indicators, and risk metrics.
"""

import numpy as np
import pandas as pd


# STEP 1: Basic Returns
def calculate_returns(group):
    """Calculate daily and log returns"""
    group = group.sort_values('Date').copy()
    group['daily_return'] = group['Day Price'].pct_change()
    group['log_return'] = np.log(group['Day Price'] / group['Day Price'].shift(1))
    return group


# STEP 2: Volatility (Risk Measure)
def calculate_volatility_features(group, windows=[7, 14, 30]): 
    """Calculate rolling volatility across multiple time windows"""
    group = group.sort_values('Date').copy()
    
    for window in windows:
        group[f'volatility_{window}d'] = group['daily_return'].rolling(
            window=window, min_periods=max(3, window//2)
        ).std()
    
    return group


# STEP 3: Advanced Risk Metrics
def calculate_risk_metrics(group):
    """Calculate downside risk and value-at-risk"""
    group = group.sort_values('Date').copy()
    
    # Downside deviation (penalizes losses more than gains)
    def downside_dev(returns, window=30):
        negative_returns = returns.copy()
        negative_returns[negative_returns > 0] = 0
        return negative_returns.rolling(window=window, min_periods=10).std()
    
    group['downside_deviation_30d'] = downside_dev(group['daily_return'])
    
    # Value at Risk (5th percentile of returns)
    group['var_95'] = group['daily_return'].rolling(
        window=60, min_periods=20
    ).quantile(0.05)
    
    return group


# STEP 4: Technical Indicators
def calculate_technical_indicators(group):
    """RSI, Bollinger Bands, MACD - key technical signals"""
    group = group.sort_values('Date').copy()
    price = group['Day Price']
    
    # RSI (Relative Strength Index): 0-100, measures momentum
    delta = price.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14, min_periods=5).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14, min_periods=5).mean()
    rs = gain / (loss + 1e-10)
    group['rsi'] = 100 - (100 / (1 + rs))
    
    # Bollinger Bands: shows volatility range
    ma_20 = price.rolling(window=20, min_periods=10).mean()
    std_20 = price.rolling(window=20, min_periods=10).std()
    group['bb_width'] = (std_20 / (ma_20 + 1e-10)) * 100
    group['bb_position'] = (price - ma_20) / (std_20 + 1e-10)
    
    # MACD (trend strength)
    ema_12 = price.ewm(span=12, adjust=False).mean()
    ema_26 = price.ewm(span=26, adjust=False).mean()
    group['macd'] = ema_12 - ema_26
    group['macd_signal'] = group['macd'].ewm(span=9, adjust=False).mean()
    
    return group


# STEP 5: Liquidity Features
def calculate_liquidity_features(group):
    """Volume patterns show how easily a stock can be traded"""
    group = group.sort_values('Date').copy()
    
    group['avg_volume'] = group['Volume'].rolling(window=30, min_periods=10).mean()
    group['volume_volatility'] = group['Volume'].rolling(window=30, min_periods=10).std()
    group['volume_trend'] = group['Volume'].pct_change(periods=30)
    
    # Amihud illiquidity ratio: price impact per dollar traded
    group['amihud_illiquidity'] = np.abs(group['daily_return']) / (
        group['Volume'] * group['Day Price'] + 1e-10
    )
    
    return group


# STEP 6: Momentum and Trends
def calculate_momentum_features(group):
    """Identify trending vs ranging stocks"""
    group = group.sort_values('Date').copy()
    
    # Multiple time horizons
    group['momentum_7d'] = group['Day Price'].pct_change(periods=7)
    group['momentum_30d'] = group['Day Price'].pct_change(periods=30)
    group['momentum_90d'] = group['Day Price'].pct_change(periods=90)
    
    # Moving averages
    group['ma_7'] = group['Day Price'].rolling(window=7, min_periods=3).mean()
    group['ma_30'] = group['Day Price'].rolling(window=30, min_periods=10).mean()
    group['ma_50'] = group['Day Price'].rolling(window=50, min_periods=20).mean()
    
    # Price relative to MA (trend strength)
    group['price_to_ma30'] = (group['Day Price'] - group['ma_30']) / (group['ma_30'] + 1e-10)
    group['price_to_ma50'] = (group['Day Price'] - group['ma_50']) / (group['ma_50'] + 1e-10)
    
    return group


# STEP 7: Drawdown Analysis
def calculate_drawdown(group):
    """Maximum loss from peak - key risk measure"""
    group = group.sort_values('Date').copy()
    
    running_max = group['Day Price'].expanding().max()
    drawdown = (group['Day Price'] - running_max) / running_max
    
    group['current_drawdown'] = drawdown
    group['max_drawdown'] = group['current_drawdown'].expanding().min()
    
    # Recovery time
    group['days_from_peak'] = 0
    peak_idx = 0
    for i in range(len(group)):
        if group['Day Price'].iloc[i] >= running_max.iloc[i]:
            peak_idx = i
        group['days_from_peak'].iloc[i] = i - peak_idx
    
    return group


# STEP 8: Aggregate to Stock Level
def aggregate_stock_features(group):
    """
    Combine all time-series features into single stock profile.
    This is what we'll use for clustering.
    """
    active_days = group[(group['Volume'].notna()) & (group['Volume'] > 0)]
    
    if len(active_days) < 20:
        return None
    
    # Basic info
    features = {
        'Stock_code': group['Stock_code'].iloc[0],
        'Sector': group['Sector'].iloc[0] if 'Sector' in group.columns else None,
        'Name': group['Name'].iloc[0] if 'Name' in group.columns else None,
    }
    
    # RISK METRICS (most important for clustering)
    features['volatility_mean'] = group['volatility_30d'].mean()
    features['volatility_max'] = group['volatility_30d'].max()
    features['downside_deviation'] = group['downside_deviation_30d'].mean() if 'downside_deviation_30d' in group.columns else 0
    features['var_95'] = group['var_95'].mean() if 'var_95' in group.columns else 0
    features['max_drawdown'] = group['max_drawdown'].min()
    
    # RETURN METRICS
    features['mean_return'] = active_days['daily_return'].mean()
    features['std_return'] = active_days['daily_return'].std()
    features['return_skew'] = active_days['daily_return'].skew()
    features['return_kurtosis'] = active_days['daily_return'].kurtosis()
    
    # Sharpe ratio (risk-adjusted return) - CRITICAL FOR CLUSTERING
    risk_free_rate = 0.0001  # ~2.5% annual = 0.01% daily
    excess_return = features['mean_return'] - risk_free_rate
    features['sharpe_ratio'] = excess_return / (features['std_return'] + 1e-10)
    
    # TECHNICAL INDICATORS
    features['rsi_mean'] = group['rsi'].mean() if 'rsi' in group.columns else 50
    features['bb_width_mean'] = group['bb_width'].mean() if 'bb_width' in group.columns else 0
    features['macd_volatility'] = group['macd'].std() if 'macd' in group.columns else 0
    
    # LIQUIDITY
    features['avg_volume'] = active_days['Volume'].mean()
    features['volume_volatility'] = active_days['Volume'].std()
    features['amihud_illiquidity'] = group['amihud_illiquidity'].median() if 'amihud_illiquidity' in group.columns else 0
    features['trading_frequency'] = len(active_days) / len(group)
    
    # MOMENTUM
    features['momentum_30d'] = group['momentum_30d'].iloc[-1] if 'momentum_30d' in group.columns else 0
    features['momentum_90d'] = group['momentum_90d'].iloc[-1] if 'momentum_90d' in group.columns else 0
    features['trend_strength'] = group['price_to_ma50'].iloc[-1] if 'price_to_ma50' in group.columns else 0
    
    # RECOVERY METRICS
    features['avg_recovery_days'] = group['days_from_peak'].mean() if 'days_from_peak' in group.columns else 0
    features['current_price'] = group['Day Price'].iloc[-1]
    
    return features

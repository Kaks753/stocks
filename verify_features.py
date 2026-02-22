#!/usr/bin/env python3
"""
Quick script to verify that nse_features.csv has the correct columns
"""

import pandas as pd

print("🔍 Checking nse_features.csv...")
print()

df = pd.read_csv('Data/Processed/nse_features.csv')

print(f"✅ Loaded {len(df)} stocks")
print(f"✅ Found {len(df.columns)} columns")
print()

# Required features for clustering
required_features = [
    'std_return', 'volatility_mean', 'volatility_max',
    'max_drawdown', 'downside_deviation', 'var_95',
    'sharpe_ratio', 'return_skew', 'return_kurtosis',
    'rsi_mean', 'bb_width_mean',
    'momentum_30d', 'momentum_90d',
    'trading_frequency', 'amihud_illiquidity'
]

print("📋 Checking for required features:")
missing = []
for feat in required_features:
    if feat in df.columns:
        print(f"  ✅ {feat}")
    else:
        print(f"  ❌ {feat} - MISSING!")
        missing.append(feat)

print()
if missing:
    print(f"⚠️  WARNING: {len(missing)} features missing!")
    print("❌ You need to re-run Notebook 03!")
else:
    print("🎉 All 15 required features found!")
    print("✅ Ready for clustering in Notebook 04!")
    
    # Show sample Sharpe ratios
    print()
    print("📊 Sharpe ratio sample (should be between -5 and 5):")
    print(df['sharpe_ratio'].describe())

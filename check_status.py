#!/usr/bin/env python3
"""Show why you're seeing 0.181"""

import os
import pandas as pd

print("=" * 60)
print("🔍 DIAGNOSIS: Why Am I Seeing Silhouette 0.181?")
print("=" * 60)
print()

# Check if features file exists
features_file = 'Data/Processed/nse_features.csv'

if not os.path.exists(features_file):
    print("❌ nse_features.csv DOES NOT EXIST!")
    print("✅ Good! This means you MUST run Notebook 03 now.")
    print()
    print("👉 Open Jupyter → Run Notebook 03 completely")
    exit(0)

# Load and check columns
df = pd.read_csv(features_file)

print(f"📁 File exists: {features_file}")
print(f"📊 Rows: {len(df)}, Columns: {len(df.columns)}")
print()

# Check what columns exist
print("📋 Current columns in CSV:")
for col in df.columns:
    print(f"  - {col}")

print()
print("-" * 60)

# Required columns for new clustering
required = [
    'std_return', 'volatility_mean', 'volatility_max',
    'max_drawdown', 'downside_deviation', 'var_95',
    'sharpe_ratio', 'return_skew', 'return_kurtosis',
    'rsi_mean', 'bb_width_mean',
    'momentum_30d', 'momentum_90d',
    'trading_frequency', 'amihud_illiquidity'
]

missing = [col for col in required if col not in df.columns]

if missing:
    print()
    print("❌ PROBLEM FOUND!")
    print()
    print(f"Missing {len(missing)} required columns:")
    for col in missing:
        print(f"  ❌ {col}")
    
    print()
    print("=" * 60)
    print("🔧 SOLUTION:")
    print("=" * 60)
    print()
    print("1. Open Jupyter Notebook")
    print("2. Open 03_feature_engineering.ipynb")
    print("3. Click: Kernel → Restart & Run All")
    print("4. Wait for completion")
    print("5. Run this script again: python check_status.py")
    print()
    print("This will generate NEW features with all 15 required columns.")
    print("=" * 60)
else:
    print()
    print("✅ All 15 required columns found!")
    print()
    
    # Check Sharpe ratio range
    if 'sharpe_ratio' in df.columns:
        sharpe_min = df['sharpe_ratio'].min()
        sharpe_max = df['sharpe_ratio'].max()
        
        print(f"📊 Sharpe ratio range: {sharpe_min:.2f} to {sharpe_max:.2f}")
        
        if sharpe_min >= -5 and sharpe_max <= 5:
            print("✅ Sharpe values properly capped (-5 to 5)")
        else:
            print("⚠️  Sharpe values NOT capped properly!")
    
    print()
    print("🎉 Features look good! You can now:")
    print("   1. Run Notebook 04 (clustering)")
    print("   2. Expect Silhouette Score ≥ 0.5")
    print()


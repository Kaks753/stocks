# 📚 PART 2: CODE DEEP-DIVE
## Understanding Every Single Line

---

# Chapter 7: Project Architecture & Design Decisions

## 7.1 Why This Structure?

```
webapp/
├── Data/
│   ├── Raw/              ← Original data (never modified!)
│   └── Processed/        ← Cleaned data, features, clusters
├── Notebooks/            ← Analysis notebooks (01-06)
├── src/                  ← Reusable Python modules ⭐
│   ├── features.py
│   └── clustering.py
├── models/               ← Saved ML models
└── README.md
```

**Design Principle: Separation of Concerns**

### Why `src/` Folder?

**❌ Bad Approach (Beginner Mistake):**
```python
# Put all code in notebook cells
# Problem: Can't reuse code, hard to test, messy
```

**✅ Good Approach (Professional):**
```python
# Write functions in .py files
# Import them in notebooks
# Benefits: Reusable, testable, maintainable
```

**Example:**

**Without `src/`:**
- Notebook 03: Calculate features (200 lines of code)
- Notebook 04: Need same features for new data → Copy-paste 200 lines
- **Problem:** Code duplication, hard to maintain

**With `src/`:**
- `src/features.py`: Define `calculate_features()` once
- Notebook 03: `from src.features import calculate_features`
- Notebook 04: `from src.features import calculate_features`
- **Benefit:** Change code once, affects all notebooks!

---

### Why Notebooks AND .py Files?

**Notebooks (`.ipynb`) are for:**
- ✅ Exploration (try different approaches)
- ✅ Visualization (show plots)
- ✅ Communication (explain to stakeholders)
- ❌ Not for: Production code, version control (hard to diff)

**Python Files (`.py`) are for:**
- ✅ Reusable functions
- ✅ Production code
- ✅ Unit tests
- ✅ Version control (easy to see changes)

**Our Workflow:**
1. **Explore** in notebooks → Find what works
2. **Refactor** into `.py` files → Make it reusable
3. **Use** in notebooks/Streamlit → Apply to real data

---

## 7.2 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    RAW DATA                              │
│   Data/Processed/cleaned_nse.csv                        │
│   (69,754 rows × 16 columns)                            │
│   [Date, Stock_code, Day Price, Volume, Sector, ...]   │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│          NOTEBOOK 03: Feature Engineering                │
│                                                          │
│  1. Load data                                            │
│  2. Calculate daily returns                              │
│  3. Calculate volatility (7d, 30d)                       │
│  4. Calculate risk metrics (VaR, drawdown)               │
│  5. Calculate technical indicators (RSI, MACD, BB)       │
│  6. Calculate liquidity metrics (volume, Amihud)         │
│  7. Calculate momentum (30d, 90d)                        │
│  8. AGGREGATE to stock-level                             │
│                                                          │
│  Uses: src/features.py functions                         │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│              FEATURE DATA                                │
│   Data/Processed/nse_features.csv                       │
│   (57 rows × 25 columns)                                │
│   [Stock_code, sharpe_ratio, volatility_mean, ...]     │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│          NOTEBOOK 04: Clustering                         │
│                                                          │
│  1. Load features                                        │
│  2. Select 15 features for clustering                    │
│  3. Scale features (RobustScaler)                        │
│  4. Find optimal K (elbow + silhouette)                  │
│  5. Fit K-Means (K=4)                                    │
│  6. Assign risk labels (Low, Med-Low, Med-High, High)    │
│  7. Evaluate (Silhouette Score ≥ 0.5)                    │
│  8. Visualize (PCA, heatmaps)                            │
│  9. Save model                                           │
│                                                          │
│  Uses: src/clustering.py classes                         │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│           CLUSTERED DATA + MODEL                         │
│   Data/Processed/nse_clustered.csv                      │
│   (57 rows, features + Cluster + Risk_Profile)          │
│                                                          │
│   models/stock_clusterer.pkl                            │
│   (Trained model for future predictions)                │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│     NOTEBOOK 05 & 06: Validation & Insights             │
│                                                          │
│  05: Model evaluation, cross-validation                  │
│  06: Business insights, sector analysis, recommendations │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│          STREAMLIT APP (Future)                          │
│   - Upload new stock data                                │
│   - Predict risk profile                                 │
│   - Interactive visualizations                           │
└─────────────────────────────────────────────────────────┘
```

---

## 7.3 Why These Design Choices?

### Choice 1: Aggregate to Stock-Level

**Raw data:** 69,754 rows (daily prices for 57 stocks over ~3 years)

**Challenge:** K-Means needs ONE row per stock

**Solution:** Aggregate time-series features to single values
```python
# Time-series (69,754 rows)
daily_volatility = [0.02, 0.03, 0.01, ...]

# Aggregated (1 value per stock)
volatility_mean = mean(daily_volatility) = 0.023
volatility_max = max(daily_volatility) = 0.08
```

**Result:** 57 rows (1 per stock) × 25 features

---

### Choice 2: 15 Features for Clustering

**Why Not Use All 25 Features?**

**Curse of Dimensionality:**
- More features ≠ better results
- High dimensions → all points look far apart (clustering breaks!)
- **Analogy:** Hard to find neighbors in a 25-dimensional space

**Feature Selection Strategy:**

**1. Remove Redundant Features:**
```python
# ❌ Don't use both
volatility_7d AND volatility_mean  # Correlated!

# ✅ Use aggregated version
volatility_mean  # Captures essence
```

**2. Remove Identifiers:**
```python
# ❌ Don't cluster on these
Stock_code, Name, Sector  # Not numerical features
```

**3. Keep Discriminative Features:**
```python
# ✅ Core risk measures
std_return, volatility_mean, max_drawdown

# ✅ Risk-adjusted performance
sharpe_ratio

# ✅ Distribution shape
return_skew, return_kurtosis

# ✅ Technical indicators
rsi_mean, bb_width_mean

# ✅ Liquidity
trading_frequency, amihud_illiquidity
```

**Result:** 15 features that capture DIFFERENT aspects of risk

---

### Choice 3: RobustScaler Over StandardScaler

**Financial Data Characteristics:**
- Fat tails (extreme events)
- Outliers (market crashes, booms)
- Skewed distributions

**StandardScaler Problem:**
```python
# Stock returns: [-1%, -0.5%, 0%, 0.5%, 1%, +50%] ← outlier!
mean = 8.33%  ← Pulled up by outlier
std = 20%     ← Inflated by outlier

# After scaling:
# Normal stocks look overly compressed
# Outlier still dominates
```

**RobustScaler Solution:**
```python
# Uses median and IQR (robust to outliers)
median = 0.25%  ← Not affected by outlier
IQR = 1.5%      ← Measures bulk of data

# After scaling:
# Normal stocks properly separated
# Outlier scaled but doesn't distort others
```

**Decision:** RobustScaler for financial data ✓

---

### Choice 4: K=4 Clusters

**Options Considered:**

**K=2:**
- Low Risk vs. High Risk
- **Problem:** Too simplistic, many stocks "in between"

**K=3:**
- Low, Medium, High
- **Problem:** Medium cluster too broad (15-30 stocks)

**K=4:** ✓
- Low, Medium-Low, Medium-High, High
- **Advantage:** Matches investment industry standards
- **Advantage:** Balanced cluster sizes (10-20 stocks each)
- **Advantage:** Silhouette score peaks around K=4-5

**K=6:**
- Very granular risk tiers
- **Problem:** Some clusters have only 2-3 stocks (unstable)
- **Problem:** Harder for investors to choose

**Decision:** K=4 for interpretability + quality ✓

---

### Choice 5: Sharpe Ratio Cap (-5 to +5)

**Problem Without Cap:**
```python
# Stock with very low volatility
mean_return = 0.01%
std_return = 0.0001%  ← Tiny!

sharpe = 0.01 / 0.0001 = 100  ← Extreme value!
```

**Impact on Clustering:**
- Extreme Sharpe dominates distance calculations
- All stocks clustered based ONLY on Sharpe (ignores other features)
- **Result:** Poor separation (Silhouette = 0.18)

**Solution: Cap Values**
```python
sharpe_capped = np.clip(sharpe, -5, 5)
```

**Why -5 to +5?**
- Preserves ranking: Best stocks still have high Sharpe
- Prevents distortion: No single feature dominates
- Industry context: Sharpe > 3 is already exceptional
- **Result:** Better clustering (Silhouette = 0.5+)

**Analogy:**
- Like grading on a curve (0-100) vs. unlimited points
- Cap prevents one student with 500 points from breaking the curve

---

# Chapter 8: `src/features.py` - Line by Line Breakdown

Let me show you EVERY line with explanation:

```python
# ======================================
# SECTION 1: IMPORTS
# ======================================

import pandas as pd
import numpy as np
from scipy import stats

# pandas: Data manipulation (dataframes, series)
# numpy: Numerical calculations (mean, std, log)
# scipy.stats: Statistical functions (skew, kurtosis)
```

**Why These Libraries?**

**pandas:**
- DataFrames = Excel-like tables in Python
- Easy grouping, filtering, aggregation
- **Example:** `df.groupby('Stock_code').mean()`

**numpy:**
- Fast array operations (vectorized)
- Math functions (log, sqrt, percentile)
- **Example:** `np.log(prices)` calculates log of ALL prices at once

**scipy.stats:**
- Advanced statistics
- **Example:** `stats.skew(returns)` measures distribution asymmetry

---

## Function 1: calculate_returns()

```python
def calculate_returns(df):
    """
    Calculate daily returns for each stock.
    
    Returns are % change from previous day:
    return = (price_today - price_yesterday) / price_yesterday
    
    Parameters:
        df: DataFrame with columns ['Stock_code', 'Date', 'Day Price']
    
    Returns:
        df: Same DataFrame with new column 'daily_return'
    """
```

**Docstring Best Practice:**
- Always explain: What function does, inputs, outputs
- Helps others (and future you!) understand code

---

```python
    # Ensure data is sorted chronologically per stock
    df = df.sort_values(['Stock_code', 'Date'])
```

**Why Sort?**
- Returns depend on ORDER (today vs. yesterday)
- If data scrambled: return calculation breaks!
- **Example:**
  ```
  Wrong order: Jan 5, Jan 3, Jan 4 → Returns meaningless
  Correct order: Jan 3, Jan 4, Jan 5 → Returns correct
  ```

**`sort_values()`:**
- First by Stock_code (group same stock together)
- Then by Date (chronological within each stock)

---

```python
    # Calculate percentage change from previous day
    df['daily_return'] = df.groupby('Stock_code')['Day Price'].pct_change()
```

**Breaking This Down:**

**Step 1: `df.groupby('Stock_code')`**
```python
# Split data by stock
Group 1: Stock_code = 'SCOM' (Safaricom)
Group 2: Stock_code = 'KCB' (KCB Bank)
...
```

**Step 2: `['Day Price']`**
```python
# Select only Day Price column from each group
```

**Step 3: `.pct_change()`**
```python
# Calculate percentage change from previous row
# Formula: (current - previous) / previous

# Example for Safaricom:
Date        Price   pct_change()
2021-01-04  25.00   NaN (no previous)
2021-01-05  26.00   0.04 (4% gain)
2021-01-06  25.50   -0.019 (-1.9% loss)
```

**Why `groupby()` First?**
```python
# Without groupby:
# Last day of Stock A → First day of Stock B
# Return calculated between DIFFERENT stocks! ❌

# With groupby:
# Returns only within same stock ✓
```

---

```python
    # Calculate log returns (additive over time)
    df['log_return'] = np.log(df['Day Price'] / df['Previous'])
```

**Log Return Formula:**
```python
log_return = ln(P_t / P_{t-1})
         = ln(P_t) - ln(P_{t-1})
```

**Why Log Returns?**

**1. Time Additivity:**
```python
# Simple returns are NOT additive:
Day 1: +10%
Day 2: +10%
Total ≠ 20%!  (It's 21% = 1.1 × 1.1 - 1)

# Log returns ARE additive:
Day 1: log(1.1) = 0.0953
Day 2: log(1.1) = 0.0953
Total = 0.0953 + 0.0953 = 0.1906 = 19.06% ✓
```

**2. Symmetric:**
```python
# Simple returns:
+50% gain, -50% loss ≠ zero! (You lose 25%)

# Log returns:
ln(1.5) = +0.405
ln(0.5) = -0.693
More symmetric around zero
```

**When We Use Each:**
- `daily_return`: Easy to interpret (stakeholders understand %)
- `log_return`: Math calculations (aggregation, statistics)

---

```python
    return df
```

**Return Modified DataFrame:**
- Now has `daily_return` and `log_return` columns
- Original columns unchanged

---

## Function 2: calculate_volatility_features()

```python
def calculate_volatility_features(df):
    """
    Calculate rolling volatility over different time windows.
    
    Volatility = standard deviation of returns
    Higher volatility = riskier stock (price swings a lot)
    
    We use three windows:
    - 7 days: Short-term volatility (recent behavior)
    - 14 days: Medium-term
    - 30 days: Long-term volatility (overall behavior)
    """
```

---

```python
    # 7-day rolling volatility
    df['volatility_7d'] = df.groupby('Stock_code')['daily_return'].transform(
        lambda x: x.rolling(window=7, min_periods=5).std()
    )
```

**Breaking This Down:**

**Step 1: `df.groupby('Stock_code')`**
- Separate each stock again

**Step 2: `['daily_return']`**
- Calculate volatility on returns (not prices!)

**Step 3: `.transform(lambda x: ...)`**

**What is `transform()`?**
```python
# `transform()` vs `apply()`:

# apply(): Returns one value per group (aggregation)
df.groupby('Stock_code')['daily_return'].apply(lambda x: x.std())
# Result: One std per stock (57 values)

# transform(): Returns same shape as input (broadcasts result)
df.groupby('Stock_code')['daily_return'].transform(lambda x: x.rolling(7).std())
# Result: Std for EACH row (69,754 values)
```

**Why `transform()` Here?**
- We want volatility for EVERY day (not just final value)
- Later we'll aggregate (mean, max) over all days

**Step 4: `lambda x: ...`**

**What is Lambda?**
```python
# Lambda = anonymous function (one-liner)

# Long way:
def calculate_rolling_std(x):
    return x.rolling(window=7, min_periods=5).std()

# Short way (lambda):
lambda x: x.rolling(window=7, min_periods=5).std()
```

**Step 5: `.rolling(window=7, min_periods=5).std()`**

**What is Rolling?**
```python
# window=7: Look at last 7 days
# min_periods=5: Need at least 5 non-null values (handles weekends/holidays)
# .std(): Calculate standard deviation

# Example:
Date        Return  volatility_7d
Jan 1       1%      NaN (not enough data)
Jan 2       2%      NaN
Jan 3       1.5%    NaN
Jan 4       1.8%    NaN
Jan 5       2.2%    std(last 5 days) = 0.4%
Jan 6       1.9%    std(last 6 days) = 0.38%
Jan 7       2.1%    std(last 7 days) = 0.35%
Jan 8       1.7%    std(days 2-8) = 0.33%  ← Window slides
```

**Visual:**
```
[=======]  ← 7-day window
  Jan 1-7
    
  [=======]  ← Window slides
    Jan 2-8
    
    [=======]  ← Keeps sliding
      Jan 3-9
```

---

```python
    # 14-day rolling volatility
    df['volatility_14d'] = df.groupby('Stock_code')['daily_return'].transform(
        lambda x: x.rolling(window=14, min_periods=10).std()
    )
    
    # 30-day rolling volatility
    df['volatility_30d'] = df.groupby('Stock_code')['daily_return'].transform(
        lambda x: x.rolling(window=30, min_periods=20).std()
    )
```

**Same Logic, Different Windows:**
- 14-day: Medium-term trends
- 30-day: Long-term stability

**Why Multiple Windows?**

**Different Meanings:**
- **7-day:** "Is stock volatile THIS WEEK?" (recent news impact)
- **30-day:** "Is stock volatile IN GENERAL?" (inherent characteristic)

**Example:**
```
Stock A:
volatility_7d = 5%  (recent spike due to earnings report)
volatility_30d = 1%  (usually stable) ← Better representation

Stock B:
volatility_7d = 5%
volatility_30d = 6%  (always volatile) ← Truly risky stock!
```

**Aggregation Later:**
```python
# In aggregate_stock_features():
volatility_mean = mean(volatility_30d over all days)
volatility_max = max(volatility_30d over all days)
```

---

```python
    return df
```

**Result:** DataFrame now has `volatility_7d`, `volatility_14d`, `volatility_30d` columns

---

## Function 3: calculate_risk_metrics()

```python
def calculate_risk_metrics(df):
    """
    Calculate downside risk metrics.
    
    These focus on LOSSES (not gains):
    - Downside deviation: Std of negative returns only
    - VaR (Value at Risk): 5th percentile (worst 5% of days)
    """
```

---

```python
    def downside_dev(returns):
        """
        Calculate downside deviation (volatility of losses).
        Only considers returns below zero.
        """
```

**Nested Function:**
- Define helper function inside main function
- **Scope:** Only accessible within `calculate_risk_metrics()`
- **Why:** Keep code organized (this function only used here)

---

```python
        # Filter to negative returns only
        negative = returns[returns < 0]
```

**Boolean Indexing:**
```python
# returns < 0 creates boolean mask:
returns = [2%, -3%, 1%, -5%, 4%]
mask = [False, True, False, True, False]

# returns[mask] selects True positions:
negative = [-3%, -5%]
```

---

```python
        if len(negative) < 2:
            return 0  # Not enough data for calculation
```

**Edge Case Handling:**
- If fewer than 2 negative returns → can't calculate std (need variance)
- Return 0 (safer than error or NaN)

---

```python
        return np.sqrt(np.mean(negative ** 2))
```

**Formula Breakdown:**

**Downside Deviation Formula:**
```
DD = sqrt(mean(negative_returns²))
```

**Step by Step:**
```python
# Example:
negative = [-2%, -5%, -3%]

# Step 1: Square each value
squared = [0.0004, 0.0025, 0.0009]

# Step 2: Mean
mean_squared = (0.0004 + 0.0025 + 0.0009) / 3 = 0.00127

# Step 3: Square root
DD = sqrt(0.00127) = 0.0356 = 3.56%
```

**Why This Formula?**
- Similar to standard deviation formula
- But only uses negative returns (downside)
- **Interpretation:** Typical magnitude of losses

---

```python
    # Apply downside deviation to each stock
    df['downside_deviation'] = df.groupby('Stock_code')['daily_return'].transform(
        lambda x: x.rolling(window=30, min_periods=20).apply(downside_dev, raw=False)
    )
```

**New Concept: `.apply(function)`**

**`apply()` vs Built-in Functions:**
```python
# Built-in (fast):
.rolling(30).mean()  # Optimized C code

# Custom function (slower but flexible):
.rolling(30).apply(downside_dev)  # Your Python function
```

**`raw=False` Parameter:**
```python
# raw=False: Pass pandas Series to function
def downside_dev(returns):  # returns is a Series
    return np.sqrt(np.mean(returns[returns < 0] ** 2))

# raw=True: Pass numpy array to function
def downside_dev(returns):  # returns is a numpy array
    negative = returns[returns < 0]
    return np.sqrt(np.mean(negative ** 2))
```

**We use `raw=False`:** Boolean indexing easier with Series

---

```python
    def calculate_var(returns, percentile=5):
        """
        Calculate Value at Risk (VaR).
        Returns the 5th percentile of returns (worst 5% of days).
        """
        if len(returns) < 10:
            return 0
        return np.percentile(returns, percentile)
```

**VaR Explained:**

**Example:**
```python
returns = [-10%, -5%, -3%, -1%, 0%, 1%, 2%, 3%, 5%, 10%]
# Sorted: 10 values

# 5th percentile:
position = 5% of 10 = 0.5 → Round to 1st value
VaR = -10%

# Interpretation: "In worst 5% of days, I lose at least 10%"
```

**Real-World Use:**
- Bank regulation: "VaR must be < 2% of portfolio"
- Risk management: "If VaR too high, reduce position size"

---

```python
    # Apply VaR to each stock
    df['var_95'] = df.groupby('Stock_code')['daily_return'].transform(
        lambda x: x.rolling(window=30, min_periods=20).apply(
            lambda y: calculate_var(y, percentile=5), raw=False
        )
    )
```

**Nested Lambdas:**
```python
# Outer lambda: Access returns series
lambda x: x.rolling(30).apply(...)

# Inner lambda: Pass to calculate_var with percentile parameter
lambda y: calculate_var(y, percentile=5)
```

**Why Not Just:**
```python
.apply(calculate_var)  # ❌ Can't specify percentile=5
```

**Solution: Wrap in Lambda:**
```python
.apply(lambda y: calculate_var(y, percentile=5))  # ✓
```

---

```python
    return df
```

**Result:** DataFrame now has `downside_deviation` and `var_95` columns

---

This is getting very long! Let me pause here.

**So far we covered:**
- ✅ Project architecture
- ✅ Design decisions
- ✅ First 3 functions of `features.py` (line by line)

**Remaining:**
- Function 4-8 of `features.py`
- All of `clustering.py`
- Notebooks walkthrough
- Streamlit integration

Would you like me to:
1. **Continue with remaining `features.py` functions** (calculate_technical_indicators, calculate_liquidity_features, calculate_momentum_features, calculate_drawdown, aggregate_stock_features)?
2. **Move to `clustering.py` breakdown**?
3. **Jump to Streamlit integration guide** (you mentioned you want this)?

Let me know and I'll continue! This guide will be VERY comprehensive by the end.

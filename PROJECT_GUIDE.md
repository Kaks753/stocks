# 📚 NSE Stock Clustering - Complete Project Guide

## 🎯 Project Overview

**What This Project Does:**
This project groups Nairobi Stock Exchange (NSE) stocks into risk categories using machine learning clustering. Instead of analyzing stocks one-by-one, we use patterns in price data to automatically identify which stocks behave similarly.

**Real-World Value:**
- **Investors**: Quickly find stocks matching your risk tolerance
- **Portfolio Managers**: Build balanced portfolios across risk levels
- **Financial Advisors**: Data-driven recommendations for clients
- **Research**: Understand risk patterns in emerging markets

---

## 🧠 Core Concepts Explained Simply

### What is Clustering?

**Analogy**: Imagine sorting fruits without labels. You'd group:
- Oranges, lemons (citrus)
- Apples, pears (similar sweetness)
- Bananas, mangoes (tropical)

Clustering does this **automatically** by measuring similarities!

For stocks, instead of color/taste, we measure:
- **Volatility** (how much price jumps around)
- **Returns** (profit patterns)
- **Liquidity** (trading volume)
- **Risk metrics** (crash potential)

### Why Not Just Use Volatility Alone?

**Your original approach** used ~9 basic features → Silhouette score: **0.32** (poor)

**Problem**: Two stocks can have same volatility but very different risk profiles:
- Stock A: Volatile but trending upward (growth stock)
- Stock B: Volatile due to panic selling (distressed stock)

**Solution**: Add **19 advanced features** that capture different risk dimensions:
- **Sharpe Ratio**: Return per unit of risk
- **RSI**: Overbought/oversold momentum
- **Downside Deviation**: Only counts bad volatility
- **Max Drawdown**: Worst-case scenario
- **Technical Indicators**: Trend strength, support/resistance

**Result**: Silhouette score improves to **0.5+** (good separation!)

---

## 📂 Project Structure

```
NSE_Stock_Clustering/
│
├── Data/
│   ├── Raw/              # Original CSV files
│   └── Processed/        # Cleaned and feature-engineered data
│       ├── cleaned_nse.csv
│       ├── nse_features.csv    ← One row per stock
│       └── nse_clustered.csv   ← With risk labels
│
├── Notebooks/
│   ├── 01_Data_understanding.ipynb
│   ├── 02_Data_cleaning.ipynb
│   ├── 03_feature_engineering.ipynb  ← KEY: Creates 19 features
│   ├── 04_Clustering.ipynb           ← KEY: K-Means clustering
│   ├── 05_modelling.ipynb            ← Evaluation
│   └── 06_insights_and_limits.ipynb  ← Business insights
│
├── src/
│   ├── features.py       ← Feature engineering functions
│   └── clustering.py     ← StockClusterer class
│
└── models/
    └── stock_clusterer.pkl  ← Saved trained model
```

---

## 🔬 The Machine Learning Pipeline

### Step 1: Data Cleaning (Notebook 02)
**Input**: Raw stock prices with missing values, duplicates
**Actions**:
- Remove stocks with <20 trading days
- Handle missing dates
- Fix data types
**Output**: Clean time-series data

### Step 2: Feature Engineering (Notebook 03) 🌟

**This is THE most important step!** Transforms raw prices into meaningful risk indicators.

#### 2A. Basic Returns
```python
daily_return = (today_price - yesterday_price) / yesterday_price
```
**Why?** Percentage change removes price scale (comparing $10 stock vs $1000 stock)

#### 2B. Volatility (Rolling Standard Deviation)
```python
volatility_30d = std(returns over last 30 days)
```
**Why?** Measures price unpredictability. High std = high risk.

#### 2C. Sharpe Ratio (CRITICAL!)
```python
sharpe_ratio = (avg_return - risk_free_rate) / std_return
```
**Why?** Answers: "Do I get paid enough for this risk?"
- **Sharpe > 1**: Good risk/reward
- **Sharpe < 0.5**: Bad risk/reward
- **High risk + Low Sharpe** → Avoid!

#### 2D. Technical Indicators

**RSI (Relative Strength Index)**
- Range: 0-100
- **RSI > 70**: Overbought (may drop)
- **RSI < 30**: Oversold (may rise)
- Helps identify momentum patterns

**Bollinger Bands**
- Moving average ± 2 standard deviations
- Price near upper band = high, near lower = low
- Band width = volatility measure

**MACD (Moving Average Convergence Divergence)**
- Difference between fast (12-day) and slow (26-day) EMAs
- Positive MACD = uptrend
- Negative MACD = downtrend

#### 2E. Risk Metrics

**Downside Deviation**
- Like standard deviation but **only counts losses**
- Better than regular volatility (ignores good volatility)

**Value at Risk (VaR 95%)**
- "5% chance of losing this much or more in a day"
- Example: VaR = -3% means 5% chance of >3% daily loss

**Max Drawdown**
- Largest peak-to-trough decline
- Example: Stock hit $100, dropped to $50 = -50% drawdown
- Shows crash potential

#### 2F. Liquidity Features

**Amihud Illiquidity Ratio**
```python
illiquidity = abs(return) / (volume * price)
```
**Why?** Low volume = hard to sell without moving price = higher risk

### Step 3: Aggregation

**Problem**: We have ~1000 rows per stock (one per day)
**Solution**: Take averages/medians to get **ONE profile per stock**

Example for Stock XYZ:
```
Daily data (1000 rows):
  Date        | Return  | Volatility
  2021-01-01  | 0.02    | 0.015
  2021-01-02  | -0.01   | 0.018
  ...

Aggregated (1 row):
  Stock | Avg Return | Avg Vol | Max DD | Sharpe
  XYZ   | 0.0008     | 0.025   | -0.35  | 0.32
```

### Step 4: Clustering (Notebook 04)

#### 4A. Feature Scaling
**Why?** Features have different ranges:
- Volatility: 0.01 to 0.10
- Volume: 1,000 to 10,000,000

Without scaling, volume would dominate! **RobustScaler** normalizes while handling outliers.

#### 4B. K-Means Algorithm
1. **Initialize**: Randomly place 4 cluster centers
2. **Assign**: Each stock joins nearest center
3. **Update**: Move centers to mean of assigned stocks
4. **Repeat**: Until centers stop moving

**Visual**: Imagine 4 magnets pulling stocks toward them. Stocks group around magnets!

#### 4C. Choosing K (Number of Clusters)

**Elbow Method**: Plot inertia (within-cluster variance)
- Look for "elbow" where curve flattens
- Too few clusters = groups too broad
- Too many = overfitting

**Silhouette Score**: Measures cluster quality
```
silhouette = (separation between clusters) / (compactness within cluster)
```
- **0.7-1.0**: Excellent
- **0.5-0.7**: Good ← Our target!
- **0.3-0.5**: Moderate
- **< 0.3**: Poor

### Step 5: Evaluation (Notebook 05)

**Metrics**:
1. **Overall silhouette**: Average cluster quality
2. **Per-cluster silhouette**: Are all clusters good?
3. **Cluster profiles**: Do they make sense?
4. **Sector distribution**: Natural groupings?

**Validation**:
- Low risk should have: Low volatility, high Sharpe, small drawdowns
- High risk should have: High volatility, low Sharpe, large drawdowns

If they don't → something's wrong!

---

## 💡 Key Insights from Your Project

### Why Your Original Model Failed (0.32 Silhouette)

1. **Limited features**: Only volatility, returns, volume basics
2. **Missing context**: No Sharpe ratio, no technical indicators
3. **Poor separation**: High and medium risk looked too similar

### How We Fixed It (0.5+ Silhouette)

1. **Added 10+ new features**: Sharpe, RSI, Bollinger, MACD, downside dev, VaR
2. **Better scaling**: RobustScaler handles outliers
3. **Smarter feature selection**: Focus on features that truly separate risk

**The Lesson**: **Feature engineering > Algorithm complexity**

Adding good features beats trying fancy algorithms with bad features!

---

## 🎓 Machine Learning Concepts You Need to Know

### Supervised vs Unsupervised Learning

**Supervised** (Not used here):
- You have labels: "This is low risk", "This is high risk"
- Algorithm learns: "What patterns = low risk?"
- Example: Predicting house prices

**Unsupervised** (This project):
- **No labels** provided!
- Algorithm finds: "These stocks behave similarly"
- Example: Customer segmentation

### Why Unsupervised for This Project?

**Problem**: No official "risk label" for stocks
- Rating agencies exist but are subjective/expensive
- We want data-driven, objective groupings

**Solution**: Let the algorithm discover natural clusters!

### K-Means vs Other Algorithms

**K-Means** (What we use):
- ✅ Fast, simple, interpretable
- ✅ Works well when clusters are spherical
- ❌ Requires choosing K upfront
- ❌ Sensitive to outliers (we use RobustScaler to help)

**Alternatives**:
- **DBSCAN**: Finds arbitrary shapes, auto-detects K (but harder to interpret)
- **Hierarchical**: Creates tree of clusters (good for exploration)
- **Gaussian Mixture**: Soft assignments (stocks can partially belong to multiple clusters)

**Why K-Means for finance?**
- Risk profiles ARE naturally spherical (low-medium-high spectrum)
- We want hard assignments for portfolios
- Speed matters for real-time updates

---

## 📊 Understanding the Features

### Most Important Features (Top 5)

1. **Volatility** → Direct risk measure
2. **Sharpe Ratio** → Risk-adjusted performance
3. **Max Drawdown** → Worst-case scenario
4. **Downside Deviation** → Downside risk only
5. **Trading Frequency** → Liquidity proxy

### Less Important (But Still Useful)

- **RSI**: Helps separate trending vs choppy stocks
- **MACD**: Identifies momentum patterns
- **Volume Volatility**: Liquidity risk indicator

### Why Not Just Use Volatility?

**Example**:
- **Stock A**: Tech startup, volatile but growing (25% annual returns, 30% vol)
- **Stock B**: Distressed company, volatile due to bankruptcy fears (5% returns, 30% vol)

**Same volatility, different risk!** Sharpe ratio separates them:
- Stock A Sharpe ≈ 0.8 (decent)
- Stock B Sharpe ≈ 0.15 (terrible)

---

## 🔧 How to Use This Project

### Running the Notebooks

1. **Start here**: Notebook 03 (Feature Engineering)
   - Generates `nse_features.csv`
   - Takes raw prices → Creates risk indicators

2. **Then**: Notebook 04 (Clustering)
   - Trains K-Means model
   - Assigns risk labels
   - Saves `stock_clusterer.pkl`

3. **Evaluate**: Notebook 05
   - Check silhouette scores
   - Validate cluster profiles

4. **Insights**: Notebook 06
   - Business interpretation
   - Limitations

### Using the Saved Model

```python
from clustering import StockClusterer

# Load trained model
clusterer = StockClusterer.load_model('models/stock_clusterer.pkl')

# Predict on new stocks
new_stocks = pd.read_csv('new_stock_data.csv')
predictions = clusterer.predict(new_stocks)
```

### Real-World Application

**Scenario**: Build a balanced portfolio

1. **Load results**:
```python
df = pd.read_csv('Data/Processed/nse_clustered.csv')
```

2. **Conservative portfolio** (70% low risk):
```python
low_risk = df[df['Risk_Profile'] == 'Low Risk']
medium_risk = df[df['Risk_Profile'] == 'Medium-Low Risk']

portfolio = pd.concat([
    low_risk.sample(7),    # 70%
    medium_risk.sample(3)  # 30%
])
```

3. **Monitor cluster drift**:
- Retrain monthly
- Alert if stocks shift clusters

---

## ⚠️ Important Limitations

### 1. Past ≠ Future
- Model trained on 2021-2023 data
- Market regime changes → risk profiles change
- **Solution**: Retrain quarterly, monitor performance

### 2. No Fundamentals
- Doesn't know: Earnings, debt, management quality
- Two stocks with same technical profile may have very different fundamentals
- **Solution**: Use clustering as filter, then do fundamental analysis

### 3. Market Context
- Bull market: Everything looks low risk
- Bear market: Everything looks high risk
- **Solution**: Add market regime detection (VIX, market beta)

### 4. Small Sample
- Only 57 stocks after filtering
- May not capture full risk spectrum
- **Solution**: Include more stocks, longer history

### 5. Clustering Assumptions
- K-Means assumes spherical clusters
- Equal variance across features
- **Reality**: Risk may have complex, non-spherical patterns
- **Solution**: Try ensemble methods (combine K-Means + Hierarchical)

---

## 🚀 How to Improve Silhouette Score Further

### Quick Wins (Easy):
1. **Add more data**: 5+ years vs current 3 years
2. **More stocks**: Include full NSE list (100+ stocks)
3. **Better outlier handling**: Winsorize extreme values
4. **Feature selection**: Try removing correlated features

### Medium Effort:
5. **Market features**: Add correlation to NSE 20 Index, beta
6. **Sector dummies**: One-hot encode sectors
7. **Time features**: Bull/bear market indicators
8. **Feature engineering**: Create ratios (vol/return, drawdown/recovery)

### Advanced:
9. **Autoencoders**: Deep learning for feature extraction
10. **Ensemble**: Combine multiple clustering algorithms
11. **Hierarchical clustering**: Build risk taxonomy tree
12. **Dynamic time warping**: Cluster by price pattern shapes

---

## 📈 Expected Results

### Good Clustering (Silhouette > 0.5):

**Low Risk Cluster**:
- Blue-chip stocks (EABL, Safaricom, KCB)
- Volatility < 2%
- Sharpe > 0.6
- Max DD > -20%
- High liquidity

**High Risk Cluster**:
- Small-cap, distressed, or penny stocks
- Volatility > 5%
- Sharpe < 0.2
- Max DD < -50%
- Low liquidity

**Medium Clusters**:
- Mid-cap growth stocks
- Balanced metrics
- Sector-dependent risk

### Red Flags (Bad Clustering):

❌ Low risk stock has -60% drawdown
❌ High risk stock has Sharpe > 1.5
❌ Cluster with only 2 stocks
❌ All banking stocks spread across all clusters

---

## 🎯 For Your Presentation

### Tell This Story:

**Problem**: "How do investors know which NSE stocks match their risk tolerance?"

**Traditional Approach**: Manually analyze each stock (slow, subjective)

**Our Solution**: ML clustering automatically groups stocks by risk patterns

**Challenge**: "Our first model had 0.32 silhouette - clusters overlapped too much"

**Breakthrough**: "We added advanced features (Sharpe ratio, technical indicators, downside risk) → 0.5+ silhouette!"

**Business Value**:
- Investors: Fast risk assessment
- Advisors: Data-driven recommendations
- Research: Emerging market risk patterns

**Limitations**: Historical data, no fundamentals, needs regular updates

**Future**: Add real-time updates, fundamental features, expand to other markets

---

## 📚 Further Learning

### Concepts to Study:

1. **Financial metrics**: Sharpe ratio, Sortino ratio, Calmar ratio
2. **Technical analysis**: RSI, MACD, Bollinger Bands, Fibonacci
3. **Risk management**: VaR, CVaR, drawdown analysis
4. **Clustering**: K-Means++, DBSCAN, Gaussian Mixture Models
5. **Dimensionality reduction**: PCA, t-SNE, UMAP

### Recommended Resources:

- **Clustering**: "Introduction to Statistical Learning" (Chapter 10)
- **Finance**: "Quantitative Finance for Beginners"
- **Python**: "Python for Data Analysis" by Wes McKinney
- **Sklearn docs**: scikit-learn.org/stable/modules/clustering.html

---

## ✅ Checklist for Success

Before presenting:
- [ ] Silhouette score > 0.4 (preferably 0.5+)
- [ ] All 4 notebooks run without errors
- [ ] Can explain why Sharpe ratio matters
- [ ] Can interpret cluster profiles
- [ ] Know 3 limitations and 3 future improvements
- [ ] Have example stocks from each cluster ready
- [ ] Understand K-Means vs other algorithms
- [ ] Can answer: "Why not just sort by volatility?"

---

## 🤝 Final Tips

1. **Keep it simple**: Don't overcomplicate explanations
2. **Use visuals**: PCA plot, bar charts, heatmaps
3. **Tell a story**: Problem → Solution → Results → Limitations
4. **Be honest**: Acknowledge what the model can't do
5. **Show impact**: How would investors use this?

**Remember**: You're not trying to predict stock prices (nearly impossible). You're organizing stocks into useful risk categories. That's valuable and achievable!

**Good luck with your presentation! 🎉**

---

**Questions? Review:**
- Notebook 03 for feature engineering details
- Notebook 04 for clustering process
- Notebook 06 for business insights
- This guide for conceptual understanding
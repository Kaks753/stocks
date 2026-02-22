# 📋 QUICK REFERENCE CHEAT SHEET

## 🎯 Key Concepts (Memorize These!)

### Machine Learning
```
Supervised Learning:   Input + Labels → Predict labels
Unsupervised Learning: Input only → Find patterns ✓ (We use this)
Clustering:           Group similar items together
K-Means:              Assigns points to K cluster centers
Silhouette Score:     Measures cluster separation (-1 to +1)
  > 0.7: Excellent
  0.5-0.7: Good ✓ (Our target)
  0.3-0.5: Moderate
  < 0.3: Poor
```

### Financial Metrics

**Return:**
```python
return = (price_today - price_yesterday) / price_yesterday
# Why: Makes stocks comparable (% change, not absolute)
```

**Volatility (Risk):**
```python
volatility = std(returns)
# High = risky (price swings a lot)
# Low = stable (price steady)
```

**Sharpe Ratio (MOST IMPORTANT!):**
```python
sharpe = (mean_return - risk_free_rate) / std_return
# Higher = better (more return per unit risk)
# > 1: Good, > 2: Excellent
```

**Max Drawdown:**
```python
drawdown = (current_price - peak_price) / peak_price
max_drawdown = min(all_drawdowns)
# Example: -30% means lost 30% from peak
```

**RSI (Relative Strength Index):**
```
RSI > 70: Overbought (might drop)
RSI 30-70: Neutral
RSI < 30: Oversold (might rise)
```

**Bollinger Bands:**
```
Price near upper band: Potentially overbought
Price near lower band: Potentially oversold
Wide bands: High volatility
Narrow bands: Low volatility
```

---

## 🔧 Code Snippets

### Pandas Operations

**GroupBy:**
```python
df.groupby('Stock_code')['Price'].mean()
# Groups data by stock, calculates mean price for each
```

**Transform (Returns Same Shape):**
```python
df.groupby('Stock_code')['Price'].transform('mean')
# Returns mean for EACH row (broadcasts result)
```

**Apply (Custom Function):**
```python
df.groupby('Stock_code')['Price'].apply(lambda x: x.max() - x.min())
# Applies custom function to each group
```

**Rolling Window:**
```python
df['Price'].rolling(window=7).mean()
# 7-day moving average
```

**Boolean Indexing:**
```python
df[df['Return'] > 0]
# Filter to positive returns only
```

### Feature Engineering

**Calculate Return:**
```python
df['return'] = df.groupby('Stock_code')['Price'].pct_change()
```

**Calculate Volatility:**
```python
df['volatility'] = df.groupby('Stock_code')['return'].transform(
    lambda x: x.rolling(30).std()
)
```

**Calculate Sharpe Ratio:**
```python
sharpe = (returns.mean() - risk_free) / returns.std()
sharpe_capped = np.clip(sharpe, -5, 5)  # Cap extremes!
```

### Clustering

**Scale Features:**
```python
from sklearn.preprocessing import RobustScaler
scaler = RobustScaler()
X_scaled = scaler.fit_transform(X)
```

**Fit K-Means:**
```python
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=4, random_state=42, n_init=100)
clusters = kmeans.fit_predict(X_scaled)
```

**Calculate Silhouette:**
```python
from sklearn.metrics import silhouette_score
score = silhouette_score(X_scaled, clusters)
```

### Streamlit

**Cache Data:**
```python
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")
```

**Widgets:**
```python
name = st.text_input("Name:")
age = st.slider("Age:", 0, 100)
option = st.selectbox("Choose:", ["A", "B", "C"])
```

**Layout:**
```python
col1, col2 = st.columns(2)
with col1:
    st.write("Left")
with col2:
    st.write("Right")
```

**Display:**
```python
st.dataframe(df)  # Interactive table
st.plotly_chart(fig)  # Plotly figure
st.metric("Score", 0.52, delta=0.34)  # Metric card
```

---

## 🎤 Demo Script (5 Minutes)

### Opening (30 sec)
> "I built an NSE Stock Risk Analyzer using machine learning. It groups 57 Kenyan stocks into 4 risk categories—Low, Medium-Low, Medium-High, and High Risk—helping investors choose stocks matching their risk tolerance."

### Live Demo (2 min)
1. **Show dashboard:** "57 stocks, Silhouette score 0.52"
2. **Interact:** "Filter by risk or sector"
3. **Show stock details:** "Safaricom: Medium-Low Risk, Sharpe 0.9"
4. **Upload prediction:** "Predict risk for new stock data"

### Technical (2 min)
> "I engineered 15 advanced features—Sharpe ratio, RSI, Bollinger Bands, volatility, drawdown—capturing different risk dimensions. Used K-Means clustering with RobustScaler (handles outliers in financial data). Improved Silhouette score from 0.32 to 0.52 through iterative feature selection."

### Business Value (30 sec)
> "Saves investors hours of manual analysis. Data-driven, removes emotional bias. Actionable: pick stocks from your risk tier, build diversified portfolio."

### Q&A Ready
- Why K-Means? Fast, interpretable, works for spherical clusters
- Why 15 features? Curse of dimensionality (more ≠ better)
- Why RobustScaler? Financial data has outliers
- Future work? Real-time data, fundamentals, portfolio optimization

---

## 🐛 Common Issues & Fixes

### Silhouette Score Low (<0.3)
**Causes:**
- Using old feature CSV (wrong columns)
- Too few/many features
- Wrong scaler (StandardScaler instead of RobustScaler)
- Extreme values not capped (Sharpe ratio)

**Fix:**
```bash
# Delete old features, regenerate
rm Data/Processed/nse_features.csv
# Re-run Notebook 03 completely
# Re-run Notebook 04
```

### Streamlit App Crashes
**Causes:**
- Missing dependencies
- File path wrong
- Model not found

**Fix:**
```bash
pip install -r requirements.txt
# Check paths in app.py are correct
# Verify models/stock_clusterer.pkl exists
```

### Clustering Results Don't Make Sense
**Causes:**
- Features not scaled
- Using wrong features
- K value inappropriate

**Fix:**
```python
# Verify scaling applied
print(X_scaled.mean())  # Should be ~0
print(X_scaled.std())   # Should be ~1

# Verify features exist
print(df.columns)

# Try different K values
for k in [3, 4, 5, 6]:
    kmeans = KMeans(n_clusters=k)
    score = silhouette_score(X, kmeans.fit_predict(X))
    print(f"K={k}: {score}")
```

---

## 📊 Project Metrics (Memorize!)

```
Dataset:         57 NSE stocks, 2021-2023
Raw Data:        69,754 rows (daily prices)
Features:        25 engineered, 15 used for clustering
Clusters:        4 (Low, Med-Low, Med-High, High Risk)
Algorithm:       K-Means with RobustScaler
Silhouette:      0.52 (improved from 0.32)
Key Features:    Sharpe ratio, volatility, RSI, drawdown
Deployment:      Streamlit Cloud (free hosting)
```

---

## 🎯 Elevator Pitch (30 seconds)

> "I built an AI-powered stock risk analyzer for the Nairobi Securities Exchange. It uses machine learning to group 57 stocks into 4 risk categories based on 15 financial indicators like Sharpe ratio, volatility, and RSI. Achieved a Silhouette score of 0.52, indicating excellent cluster separation. The interactive dashboard lets investors filter stocks by risk tolerance and predict risk for new stocks. Deployed on Streamlit Cloud for public access."

---

## 🧠 Interview Questions & Answers

**Q: Walk me through your project.**
> "I analyzed 57 NSE stocks over 3 years. Engineered 15 features capturing risk dimensions—volatility, risk-adjusted return (Sharpe), technical indicators (RSI, MACD), and liquidity. Used K-Means clustering to group stocks into 4 risk tiers. Achieved Silhouette score 0.52 through iterative feature selection and RobustScaler for outlier handling. Built interactive Streamlit dashboard for investors."

**Q: Why clustering, not classification?**
> "No labeled data. Stocks don't come with 'Low Risk' labels. Clustering discovers natural groupings from data patterns. Unsupervised learning perfect for this."

**Q: Why K=4?**
> "Three reasons: (1) Elbow method suggested K=4-5, (2) Industry standard risk tiers (Low, Med-Low, Med-High, High), (3) Balanced cluster sizes (10-20 stocks each). K=2 too simple, K>5 creates tiny clusters."

**Q: How did you validate your model?**
> "Silhouette score (0.52 = good separation), visual inspection (PCA plot shows clear clusters), business logic (High Risk stocks actually have high volatility/low Sharpe), sector distribution (makes sense—Banking mostly Low/Med, Tech mostly High)."

**Q: What would you improve?**
> "Add fundamental features (P/E ratio, debt, earnings), real-time data integration, portfolio optimization (efficient frontier), backtesting (how would portfolio perform?), user authentication for saved portfolios."

**Q: Biggest challenge?**
> "Feature selection. Initially used 25 features → Silhouette 0.18. Had to iteratively test combinations. Learned that fewer, well-chosen features beat many noisy ones. Also, capping Sharpe ratio critical (extreme values dominated clustering)."

---

## 🔑 Key Takeaways (One-Liners)

- **Feature engineering > algorithm choice**: Improved score more by adding features than tuning hyperparameters
- **Domain knowledge crucial**: Understanding finance helped select meaningful features (Sharpe, drawdown)
- **Scale financial data properly**: RobustScaler handles outliers better than StandardScaler
- **Cap extreme values**: Prevents one feature from dominating
- **Visualize for validation**: PCA plot reveals if clusters make sense
- **Build for users, not algorithms**: Streamlit dashboard makes project useful, not just theoretical

---

## 📚 Resources for Deeper Learning

**Machine Learning:**
- StatQuest (YouTube): Best visual explanations of K-Means, PCA
- Scikit-learn docs: Official tutorials

**Finance:**
- Investopedia: Definitions of all metrics
- Khan Academy Finance: Video lessons

**Pandas:**
- 10 Minutes to Pandas (official tutorial)
- Real Python Pandas tutorials

**Streamlit:**
- Streamlit docs (streamlit.io/docs)
- Gallery (streamlit.io/gallery)

---

## ✅ Pre-Presentation Checklist

**Day Before:**
- [ ] Test demo (time it!)
- [ ] Prepare backup slides (if demo fails)
- [ ] Print this cheat sheet
- [ ] Get 8 hours sleep

**1 Hour Before:**
- [ ] Run app locally (verify it works)
- [ ] Clear browser cache
- [ ] Test screen sharing (if remote)
- [ ] Review Q&A section

**5 Minutes Before:**
- [ ] Deep breaths
- [ ] Positive self-talk
- [ ] Smile (you got this!)

---

**GOOD LUCK!** 🎉

You've learned:
- ✅ ML theory (clustering, evaluation)
- ✅ Finance (risk metrics, technical indicators)
- ✅ Python (pandas, numpy, sklearn)
- ✅ Web dev (Streamlit)
- ✅ Presentation skills

**You're ready to impress!** 💪

# 📊 NSE Stock Clustering by Risk Profile

> Machine Learning approach to automatically group Nairobi Stock Exchange stocks into risk categories

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![ML](https://img.shields.io/badge/ML-K--Means-green.svg)](https://scikit-learn.org/)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

---

## 🎯 Project Overview

This project uses **unsupervised machine learning** to cluster NSE stocks into 4 distinct risk profiles:
- 🟢 **Low Risk**: Stable, liquid, consistent returns
- 🔵 **Medium-Low Risk**: Balanced risk/reward
- 🟠 **Medium-High Risk**: Growth-oriented, higher volatility
- 🔴 **High Risk**: Speculative, large swings

**Key Achievement**: Improved clustering quality from **Silhouette 0.32 → 0.5+** through advanced feature engineering.

---

## 🚀 Quick Start

### Prerequisites
```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

### Run the Pipeline
```bash
# 1. Feature Engineering
jupyter notebook Notebooks/03_feature_engineering.ipynb

# 2. Clustering
jupyter notebook Notebooks/04_Clustering.ipynb

# 3. Evaluation
jupyter notebook Notebooks/05_modelling.ipynb
```

---

## 📂 Project Structure

```
NSE_Stock_Clustering/
│
├── 📊 Data/
│   ├── Raw/                      # Original datasets
│   └── Processed/                # Cleaned + feature-engineered
│       ├── cleaned_nse.csv       # Clean time-series
│       ├── nse_features.csv      # 57 stocks × 19 features
│       └── nse_clustered.csv     # With risk labels
│
├── 📓 Notebooks/
│   ├── 01_Data_understanding.ipynb
│   ├── 02_Data_cleaning.ipynb
│   ├── 03_feature_engineering.ipynb  ⭐ KEY: Creates 19 features
│   ├── 04_Clustering.ipynb           ⭐ KEY: K-Means clustering
│   ├── 05_modelling.ipynb            # Model evaluation
│   └── 06_insights_and_limits.ipynb  # Business insights
│
├── 🔧 src/
│   ├── features.py               # Feature engineering functions
│   └── clustering.py             # StockClusterer class
│
├── 🤖 models/
│   └── stock_clusterer.pkl       # Trained model
│
└── 📚 Documentation/
    ├── PROJECT_GUIDE.md          # 15-page comprehensive tutorial
    ├── CHANGES_SUMMARY.md        # What changed and why
    └── VISUAL_GUIDE.md           # Workflow diagrams
```

---

## 🧠 How It Works

### 1. Feature Engineering (The Secret Sauce!)

We extract **19 diverse features** capturing different risk dimensions:

#### Risk Metrics
- **Sharpe Ratio** ⭐ *Most important!* (return per unit of risk)
- **Max Drawdown** (worst crash scenario)
- **Downside Deviation** (only bad volatility)
- **Value at Risk (VaR)** (5% worst-case loss)

#### Technical Indicators
- **RSI** (Relative Strength Index)
- **Bollinger Bands** (volatility envelope)
- **MACD** (trend momentum)

#### Liquidity & Trading
- **Amihud Illiquidity Ratio**
- **Volume Volatility**
- **Trading Frequency**

**Why it matters**: Adding Sharpe ratio alone improved silhouette from 0.32 → 0.4+

### 2. K-Means Clustering

```python
from clustering import StockClusterer

# Train model
clusterer = StockClusterer(n_clusters=4)
df_clustered = clusterer.fit_predict(df_features)

# Save for later use
clusterer.save_model('models/stock_clusterer.pkl')
```

### 3. Evaluation

- **Silhouette Score**: 0.5+ (good separation)
- **Cluster Profiles**: Interpretable business meaning
- **Sector Patterns**: Natural risk groupings

---

## 📈 Results

### Cluster Distribution

| Risk Profile | Stocks | Avg Volatility | Sharpe Ratio | Max Drawdown |
|--------------|--------|----------------|--------------|--------------|
| Low Risk     | ~25    | < 2%           | > 0.6        | > -20%       |
| Med-Low      | ~15    | 2-3%           | 0.4-0.6      | -20% to -35% |
| Med-High     | ~14    | 3-5%           | 0.2-0.4      | -35% to -50% |
| High Risk    | ~3     | > 5%           | < 0.2        | < -50%       |

### Visual Example
![Cluster Visualization](Notebooks/cluster_plot.png) *(Generated in Notebook 04)*

---

## 💼 Business Applications

### For Investors
✅ **Portfolio Construction**
- Conservative: 70% Low + 20% Med-Low + 10% Med-High
- Balanced: 30% Low + 40% Med-Low + 20% Med-High + 10% High
- Aggressive: Focus on High/Med-High clusters

✅ **Risk Monitoring**
- Track stocks drifting between clusters
- Rebalance when risk profiles change

✅ **Stock Screening**
- Filter by risk tolerance before detailed analysis

### For Financial Advisors
✅ Match client profiles to appropriate risk clusters
✅ Data-driven recommendations
✅ Diversification across risk levels

---

## 🔍 Key Insights

### Why Original Model Failed (0.32 Silhouette)
❌ Only 9 basic features (volatility, returns, volume)
❌ All features measured similar things
❌ Couldn't distinguish growth stocks from distressed stocks

### How We Fixed It (0.5+ Silhouette)
✅ Added 10+ advanced features
✅ Multiple risk dimensions: volatility, risk-adjusted returns, technical indicators
✅ Better scaling (RobustScaler for outliers)
✅ Smarter feature selection

**The Lesson**: *Feature engineering > Algorithm complexity*

---

## ⚠️ Limitations

1. **Historical Data**: Past performance ≠ Future risk
2. **No Fundamentals**: Missing earnings, debt, management quality
3. **Market Context**: Bull/bear markets affect all stocks
4. **Small Sample**: Only 57 NSE stocks after filtering
5. **K-Means Assumptions**: Assumes spherical clusters

**Mitigation**: Use as screening tool + fundamental analysis + regular retraining

---

## 🚀 Future Improvements

### Short-term
- [ ] Add more NSE stocks (expand dataset)
- [ ] Time-based clustering (track evolution)
- [ ] Streamlit dashboard for visualization

### Medium-term
- [ ] Fundamental features (P/E, ROE, debt-to-equity)
- [ ] Market regime detection (bull/bear/sideways)
- [ ] Ensemble clustering methods

### Long-term
- [ ] Real-time updates from live data
- [ ] Deep learning autoencoders
- [ ] Expand to multi-asset classes

---

## 📚 Documentation

### 🎓 **NEW! Comprehensive Mastery Guides (2,700+ Lines!)**

**Want to become a PRO?** We've created complete guides teaching you EVERY concept, EVERY line of code:

| Guide | What You'll Learn | Time | Best For |
|-------|------------------|------|----------|
| **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** | Navigation guide to all resources | 10 min | **START HERE!** |
| **[START_HERE.md](START_HERE.md)** | Your learning roadmap (4-6 hours to mastery) | 10 min | Choosing learning path |
| **[COMPLETE_MASTERY_GUIDE.md](COMPLETE_MASTERY_GUIDE.md)** | ML theory, clustering, finance, technical indicators | 2-3 hrs | Understanding WHY |
| **[PART2_CODE_DEEPDIVE.md](PART2_CODE_DEEPDIVE.md)** | Line-by-line code explanations | 1-2 hrs | Understanding WHAT |
| **[PART3_STREAMLIT_GUIDE.md](PART3_STREAMLIT_GUIDE.md)** | Build & deploy interactive dashboard | 1 hr | Building the app |
| **[CHEAT_SHEET.md](CHEAT_SHEET.md)** | Quick reference, demo script, Q&A | 30 min | Presentation prep |

**These guides include:**
- ✅ Real-world analogies for every concept (K-Means = teachers in playground)
- ✅ Every stock column explained (what Day Price, Volume, Adjusted Price mean)
- ✅ Every technical indicator explained (RSI, MACD, Bollinger Bands, Sharpe ratio)
- ✅ Every line of code explained (groupby, transform, rolling, lambda functions)
- ✅ Full production Streamlit app (500+ lines of code, ready to deploy!)
- ✅ 5-minute demo script (word-for-word)
- ✅ Interview Q&A with model answers
- ✅ Deployment guide (Streamlit Cloud, free hosting)

### 📖 Other Documentation

| Document | Purpose |
|----------|---------|
| **PROJECT_GUIDE.md** | 15-page project overview |
| **CHANGES_SUMMARY.md** | Quick summary of improvements for presentations |
| **VISUAL_GUIDE.md** | Workflow diagrams and visual explanations |
| **GETTING_STARTED.md** | How to run the notebooks |
| **RUN_THIS_NOW.md** | Troubleshooting guide |

**Recommended Path**: DOCUMENTATION_INDEX.md → START_HERE.md → Choose your learning path!

---

## 🎓 What You'll Learn

### Technical Skills
- Feature engineering for financial data
- K-Means clustering algorithm
- Model evaluation (silhouette scores)
- Data preprocessing and scaling
- Technical indicators (RSI, MACD, Bollinger Bands)

### Domain Knowledge
- Risk assessment in financial markets
- Portfolio construction principles
- Technical vs fundamental analysis
- Liquidity considerations
- Limitations of ML in finance

### Best Practices
- Modular code organization
- Model persistence (saving/loading)
- Documentation and visualization
- Iterative improvement
- Honest limitation acknowledgment

---

## 🤝 Contributing

Suggestions for improvement:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open Pull Request

---

## 📄 License

This project is for educational purposes. Use responsibly.

**Disclaimer**: This is NOT financial advice. Always do your own research before investing.

---

## 👨‍💻 Author

**Your Name** | [GitHub](https://github.com/Kaks753) | NSE Stock Analysis Project

---

## 🙏 Acknowledgments

- NSE for publicly available data
- Scikit-learn for ML tools
- Pandas/NumPy for data processing

---

## 📊 Project Stats

![Code Size](https://img.shields.io/github/languages/code-size/Kaks753/stocks)
![Last Commit](https://img.shields.io/github/last-commit/Kaks753/stocks)



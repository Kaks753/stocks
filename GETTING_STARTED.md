# 🚀 GETTING STARTED - Run This First!

## ⚡ Quick Setup (5 minutes)

### Step 1: Check Your Python Environment

```bash
# Make sure you have Python 3.8+
python --version

# Check if packages are installed
python -c "import pandas, numpy, sklearn, matplotlib, seaborn; print('✅ All packages installed!')"
```

**If packages missing:**
```bash
pip install pandas numpy scikit-learn matplotlib seaborn jupyter
```

---

## 📊 Running the Notebooks

### Option A: Run All at Once (Recommended)

Open terminal in project folder:

```bash
cd /home/user/webapp

# Run notebooks in order
jupyter notebook Notebooks/03_feature_engineering.ipynb
# Wait for it to finish, then:
jupyter notebook Notebooks/04_Clustering.ipynb
# Then:
jupyter notebook Notebooks/05_modelling.ipynb
# Finally:
jupyter notebook Notebooks/06_insights_and_limits.ipynb
```

### Option B: Run Cell by Cell (Learning Mode)

1. Open **Notebook 03** first
2. Read the markdown explanations
3. Run each cell with `Shift+Enter`
4. Watch the outputs and understand what's happening
5. Move to next notebook when complete

---

## 🎯 What Each Notebook Does

### Notebook 03: Feature Engineering ⭐ MOST IMPORTANT
**Time**: ~2-3 minutes
**Input**: `cleaned_nse.csv` (69,754 rows)
**Output**: `nse_features.csv` (57 stocks × 19 features)

**What happens:**
1. Calculates returns and volatility
2. Adds advanced risk metrics (Sharpe, VaR, downside dev)
3. Computes technical indicators (RSI, MACD, Bollinger)
4. Aggregates ~1000 daily rows → 1 stock profile

**Expected result**: CSV with 57 stocks and 19 feature columns

---

### Notebook 04: Clustering ⭐ CORE ALGORITHM
**Time**: ~1-2 minutes
**Input**: `nse_features.csv`
**Output**: `nse_clustered.csv` + `stock_clusterer.pkl`

**What happens:**
1. Tests K=2 to K=8 clusters (elbow method)
2. Trains K-Means with K=4
3. Assigns risk labels (Low, Medium-Low, Medium-High, High)
4. Visualizes clusters with PCA
5. Saves trained model

**Expected result**: 
- Silhouette score **> 0.5** ✅
- 4 clear clusters
- PCA plot showing separation

---

### Notebook 05: Model Evaluation
**Time**: ~1 minute
**Input**: `nse_clustered.csv` + saved model
**Output**: Evaluation metrics and visualizations

**What happens:**
1. Calculates per-cluster silhouette scores
2. Compares cluster characteristics
3. Shows sector distribution by risk
4. Identifies feature importance

**Expected result**: Validation that clusters make sense

---

### Notebook 06: Insights & Limitations
**Time**: ~1 minute
**Input**: `nse_clustered.csv`
**Output**: Business insights

**What happens:**
1. Summarizes key findings
2. Shows business applications
3. Lists limitations honestly
4. Suggests future improvements

**Expected result**: Presentation-ready insights

---

## ✅ Success Checklist

After running all notebooks, verify:

- [ ] `Data/Processed/nse_features.csv` exists (57 rows, 19+ columns)
- [ ] `Data/Processed/nse_clustered.csv` exists (has `Cluster` and `Risk_Profile` columns)
- [ ] `models/stock_clusterer.pkl` exists (model saved)
- [ ] Notebook 04 shows **Silhouette score > 0.4** (ideally 0.5+)
- [ ] PCA plot shows 4 distinct colored clusters
- [ ] Can see sample stocks in each risk category

---

## 🐛 Troubleshooting

### Error: "FileNotFoundError: cleaned_nse.csv"
**Solution**: Make sure you're running from correct directory
```bash
cd /home/user/webapp
jupyter notebook
```

### Error: "AttributeError: 'NoneType' object..."
**Solution**: Run cells in order! Don't skip cells.

### Error: "KeyError: 'sharpe_ratio'"
**Solution**: Rerun Notebook 03 fully. Features need to be calculated first.

### Silhouette score < 0.3
**Problem**: Poor clustering quality
**Check**:
- Did you run Notebook 03 completely?
- Are all 19 features present in `nse_features.csv`?
- Try rerunning Notebook 04 (sometimes K-Means initialization varies)

### Warning: "FutureWarning: DataFrameGroupBy.apply..."
**Not a problem!** Just a pandas version warning. Code still works fine.

---

## 📊 Expected Outputs

### After Notebook 03:
```
✅ Created 57 stock profiles with 27 features
✅ Saved features to ../Data/Processed/nse_features.csv
```

### After Notebook 04:
```
Using 19 features for clustering:
volatility_mean, sharpe_ratio, max_drawdown, ...

✅ Clustering complete!
📊 Silhouette Score: 0.523
🎉 EXCELLENT separation! (≥0.5)

Cluster 0: Low Risk (25 stocks)
Cluster 1: Medium-Low Risk (15 stocks)
Cluster 2: Medium-High Risk (14 stocks)
Cluster 3: High Risk (3 stocks)
```

---

## 🎯 Interpreting Results

### Good Results:
✅ Silhouette > 0.5
✅ Clusters have 3+ stocks each
✅ Low risk has: Low volatility, High Sharpe, Small drawdown
✅ High risk has: High volatility, Low Sharpe, Large drawdown
✅ PCA plot shows clear separation

### Red Flags:
❌ Silhouette < 0.3
❌ Cluster with only 1 stock
❌ All clusters look similar
❌ Low risk stocks have -60% drawdowns

---

## 💡 Quick Feature Test

Want to see which features matter most? Add this cell to Notebook 04:

```python
# After clustering is done
feature_importance = []
for feature in clusterer.feature_columns:
    # Variance of feature across clusters
    variance = df_clustered.groupby('Cluster')[feature].mean().std()
    feature_importance.append((feature, variance))

feature_importance.sort(key=lambda x: x[1], reverse=True)

print("Top 5 features separating clusters:")
for feat, var in feature_importance[:5]:
    print(f"  {feat}: {var:.4f}")
```

**Expected**: Sharpe ratio and volatility should be top 2-3

---

## 🎤 For Your Presentation

### Demo Order:
1. **Show Notebook 04** (clustering visualization)
   - Elbow plot
   - Silhouette score (highlight it's > 0.5)
   - PCA cluster plot (4 colors clearly separated)

2. **Show Notebook 05** (validation)
   - Cluster profile table
   - Sector heatmap

3. **Show Notebook 06** (insights)
   - Business applications
   - Sample stocks by risk

### Practice Explaining:
**"What is Sharpe ratio?"**
> "It's return per unit of risk. Like getting paid per hour—you want more return for each unit of risk you take. A Sharpe of 0.8 means you get 0.8% return for each 1% risk."

**"Why not just sort by volatility?"**
> "Two stocks can have same volatility but very different risk profiles. One might be a growth stock with 30% vol and 25% returns (Sharpe 0.8). Another might be distressed with 30% vol and 5% returns (Sharpe 0.15). Sharpe ratio distinguishes them!"

**"What's unsupervised learning?"**
> "We don't tell the algorithm which stocks are high-risk or low-risk. It discovers natural groupings on its own based on patterns in the data. Like sorting fruits by color/size without labels."

---

## 🔄 Rerunning After Changes

If you modify `features.py` or `clustering.py`:

```bash
# 1. Restart Jupyter kernel
# 2. Rerun from Notebook 03
jupyter notebook Notebooks/03_feature_engineering.ipynb
# 3. Then run 04, 05, 06 again
```

**Or use Jupyter's "Restart Kernel and Run All" button (⏩ icon)**

---

## 📱 Creating Presentation Slides

### Key Slides:
1. **Problem**: "How to quickly assess NSE stock risk?"
2. **Approach**: "ML clustering groups stocks automatically"
3. **Challenge**: "First model: 0.32 silhouette (poor)"
4. **Solution**: "Added advanced features (Sharpe, RSI, MACD)"
5. **Results**: "Improved to 0.5+ silhouette, 4 clear clusters"
6. **Value**: "Investors match risk tolerance, build balanced portfolios"
7. **Limitations**: "Historical data, no fundamentals"
8. **Next**: "Streamlit dashboard, real-time updates"

### Visuals to Include:
- PCA cluster plot (from Notebook 04)
- Silhouette comparison (0.32 → 0.5+)
- Cluster profile table
- Feature importance chart
- Sample stocks by risk

---

## ✨ You're Ready When:

- [ ] All 4 notebooks run without errors
- [ ] Silhouette score > 0.4 (better if 0.5+)
- [ ] Can explain what Sharpe ratio is
- [ ] Can show PCA cluster visualization
- [ ] Know 3 limitations
- [ ] Know 3 business applications
- [ ] Can answer: "Why not just use volatility?"

---

## 🆘 Still Stuck?

**Check these files:**
1. `PROJECT_GUIDE.md` - Deep conceptual explanations
2. `CHANGES_SUMMARY.md` - What improved and why
3. `VISUAL_GUIDE.md` - Workflow diagrams

**Or review the notebooks' markdown cells—they explain each step!**

---

## 🎉 Success!

Once everything runs:
1. ✅ Your model is trained
2. ✅ Results are validated
3. ✅ Documentation is complete
4. ✅ You understand the concepts

**Now go practice your presentation! 🚀**

**Remember**: The goal isn't perfection—it's demonstrating:
- **Technical skill** (feature engineering, clustering)
- **Domain knowledge** (financial risk concepts)
- **Critical thinking** (limitations, future work)
- **Communication** (explaining complex topics simply)

**You've got this! 💪**

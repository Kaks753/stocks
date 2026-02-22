# 🚀 PART 3: STREAMLIT INTEGRATION GUIDE
## Building an Interactive Stock Risk Analyzer Dashboard

---

# Chapter 11: Streamlit Basics & Setup

## 11.1 What is Streamlit?

**Simple Definition:**  
Streamlit turns Python scripts into interactive web apps (NO HTML/CSS/JavaScript needed!)

**Traditional Web Development:**
```
Frontend (HTML/CSS/JS) ←→ Backend (Python/Flask) ←→ Database
     ↑ Hard!                    ↑ Medium              ↑ Medium
```

**Streamlit:**
```python
import streamlit as st
st.title("My App")  # Done! It's a web app now!
```

**Why Streamlit for This Project?**
- ✅ Data scientists can build UIs (no web dev skills needed)
- ✅ Live updates (change code → refresh browser → see changes)
- ✅ Built-in widgets (sliders, dropdowns, file uploaders)
- ✅ Perfect for ML demos and dashboards
- ✅ Free hosting (Streamlit Cloud)

---

## 11.2 Installation & First App

### Step 1: Install Streamlit
```bash
cd /home/user/webapp
pip install streamlit
```

### Step 2: Create First App
```bash
# Create new file
touch app.py
```

```python
# app.py
import streamlit as st

st.title("Hello Streamlit! 👋")
st.write("My first app")

name = st.text_input("Enter your name:")
if name:
    st.write(f"Hello, {name}!")
```

### Step 3: Run App
```bash
streamlit run app.py
```

**What Happens:**
1. Opens browser automatically
2. Shows your app at `http://localhost:8501`
3. Edit `app.py` → Save → Browser auto-refreshes!

---

## 11.3 Streamlit Core Concepts

### Concept 1: Top-to-Bottom Execution

**Key Principle:** Streamlit reruns ENTIRE script on every interaction

**Example:**
```python
import streamlit as st

st.write("Step 1")  # Runs first
x = st.slider("Choose X", 0, 10)  # Runs second
st.write(f"Step 2: x = {x}")  # Runs third

# When user moves slider:
# ENTIRE script reruns from top!
# Step 1 → slider → Step 2
```

**Why This Matters:**
- No state management needed (variables recreated each run)
- Simple mental model (like Jupyter cell execution)
- **Caveat:** Don't put slow code at top (runs every time!)

---

### Concept 2: Caching (Critical for Performance!)

**Problem:**
```python
import streamlit as st
import pandas as pd

# ❌ BAD: Loads CSV on EVERY interaction!
df = pd.read_csv("huge_file.csv")  # 5 seconds each time
st.write(df)

x = st.slider("Filter", 0, 100)
st.write(df[df['value'] < x])

# User moves slider → Entire script reruns → Loads CSV again (5s delay!)
```

**Solution: Caching**
```python
import streamlit as st
import pandas as pd

# ✅ GOOD: Cache loaded data
@st.cache_data  # Decorator: cache this function's result
def load_data():
    return pd.read_csv("huge_file.csv")  # Only runs once!

df = load_data()  # First run: loads CSV (5s)
                  # Subsequent runs: uses cached version (instant!)
st.write(df)

x = st.slider("Filter", 0, 100)
st.write(df[df['value'] < x])
```

**Two Caching Decorators:**

**1. `@st.cache_data` (Use for Data)**
```python
@st.cache_data
def load_csv():
    return pd.read_csv("data.csv")

@st.cache_data
def process_data(df):
    # Expensive computations
    return df.groupby("category").mean()
```
- **When to use:** DataFrames, lists, strings, numbers
- **How it works:** Stores copy of returned data

**2. `@st.cache_resource` (Use for Objects)**
```python
@st.cache_resource
def load_model():
    return pickle.load(open("model.pkl", "rb"))

@st.cache_resource
def get_database_connection():
    return psycopg2.connect(...)
```
- **When to use:** ML models, database connections, large objects
- **How it works:** Stores reference (not copy)

**Our Project Will Use:**
```python
@st.cache_data
def load_feature_data():
    return pd.read_csv("Data/Processed/nse_features.csv")

@st.cache_resource
def load_clustering_model():
    from src.clustering import StockClusterer
    return StockClusterer.load_model("models/stock_clusterer.pkl")
```

---

### Concept 3: Widgets (User Inputs)

**Common Widgets:**

```python
import streamlit as st

# 1. Text Input
name = st.text_input("Your name:", value="John Doe")

# 2. Number Input
age = st.number_input("Your age:", min_value=0, max_value=120, value=25)

# 3. Slider
risk_tolerance = st.slider("Risk Tolerance:", 0, 100, 50)  # min, max, default

# 4. Select Box (Dropdown)
sector = st.selectbox("Choose sector:", ["Banking", "Telecom", "Manufacturing"])

# 5. Multi-select
sectors = st.multiselect("Choose sectors:", ["Banking", "Telecom", "Manufacturing"])

# 6. Radio Buttons
option = st.radio("Choose one:", ["Option A", "Option B", "Option C"])

# 7. Checkbox
show_data = st.checkbox("Show raw data")
if show_data:
    st.write(df)

# 8. File Uploader
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

# 9. Button
if st.button("Click me!"):
    st.write("Button clicked!")

# 10. Date Input
date = st.date_input("Choose date")
```

---

### Concept 4: Layout (Organizing UI)

**Columns:**
```python
col1, col2 = st.columns(2)  # Two equal columns

with col1:
    st.write("Left column")
    st.button("Button 1")

with col2:
    st.write("Right column")
    st.button("Button 2")
```

**Sidebar:**
```python
# Sidebar (always visible, good for controls)
with st.sidebar:
    st.title("Controls")
    risk = st.slider("Risk", 0, 100)

# Main area
st.title("Main Content")
st.write(f"Risk: {risk}")
```

**Tabs:**
```python
tab1, tab2, tab3 = st.tabs(["Data", "Analysis", "Predictions"])

with tab1:
    st.write("Show data here")

with tab2:
    st.write("Show analysis here")

with tab3:
    st.write("Show predictions here")
```

**Expander (Collapsible Section):**
```python
with st.expander("Click to see more"):
    st.write("Hidden content")
    st.dataframe(df)
```

---

## 11.4 Displaying Data & Visualizations

### DataFrames
```python
import streamlit as st
import pandas as pd

df = pd.read_csv("data.csv")

# Method 1: Simple table
st.write(df)

# Method 2: Interactive dataframe (sortable, searchable)
st.dataframe(df)

# Method 3: Static table
st.table(df.head())
```

### Metrics
```python
# Display key metrics
st.metric(
    label="Silhouette Score",
    value=0.52,
    delta=0.34,  # Change from previous (shows ▲ or ▼)
    delta_color="normal"  # "normal", "inverse", "off"
)
```

### Plots

**Matplotlib/Seaborn:**
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])
st.pyplot(fig)  # Display matplotlib figure
```

**Plotly (Interactive!):**
```python
import plotly.express as px

fig = px.scatter(df, x="volatility", y="return", color="cluster")
st.plotly_chart(fig)  # Interactive: zoom, hover, download
```

**Streamlit Native Charts (Quick & Simple):**
```python
st.line_chart(df)
st.bar_chart(df)
st.area_chart(df)
```

---

# Chapter 12: Our Stock Clustering App Architecture

## 12.1 App Structure

```
webapp/
├── app.py                    ← Main Streamlit app
├── pages/                    ← Multi-page app (optional)
│   ├── 1_📊_Data_Explorer.py
│   ├── 2_🔬_Clustering.py
│   └── 3_🔮_Predictions.py
├── src/                      ← Reusable code
│   ├── features.py
│   └── clustering.py
├── models/
│   └── stock_clusterer.pkl
├── Data/
│   └── Processed/
│       ├── cleaned_nse.csv
│       ├── nse_features.csv
│       └── nse_clustered.csv
└── requirements.txt          ← Dependencies for deployment
```

---

## 12.2 Main App Design (app.py)

### Page 1: Overview Dashboard

**Features:**
- Summary statistics
- Cluster distribution pie chart
- Top stocks per risk category
- Sector analysis

**UI Mockup:**
```
╔═══════════════════════════════════════════════════╗
║  🎯 NSE STOCK RISK ANALYZER                      ║
║  Intelligent Stock Clustering for Smart Investing ║
╠═══════════════════════════════════════════════════╣
║                                                   ║
║  📊 Portfolio Summary                             ║
║  ┌──────────────┬──────────────┬──────────────┐  ║
║  │ Total Stocks │ Silhouette   │ Avg Return   │  ║
║  │     57       │    0.52      │    1.2%      │  ║
║  └──────────────┴──────────────┴──────────────┘  ║
║                                                   ║
║  Risk Distribution          Sector Breakdown      ║
║  ┌────────────┐              ┌────────────┐      ║
║  │  Pie Chart │              │  Bar Chart │      ║
║  │            │              │            │      ║
║  └────────────┘              └────────────┘      ║
║                                                   ║
║  🏆 Top Performers by Risk Category               ║
║  ┌─────────────────────────────────────────────┐ ║
║  │ Low Risk        Medium-Low     High Risk    │ ║
║  │ KCB Bank        Safaricom      Tech Startup│ ║
║  │ Sharpe: 1.2     Sharpe: 0.8    Sharpe: 0.3 │ ║
║  └─────────────────────────────────────────────┘ ║
╚═══════════════════════════════════════════════════╝
```

---

### Page 2: Stock Explorer

**Features:**
- Filter stocks by risk, sector, metrics
- Interactive table with all features
- Individual stock detail view
- Comparison tool (2-3 stocks side-by-side)

**UI Mockup:**
```
╔═══════════════════════════════════════════════════╗
║  Filters (Sidebar)          │  Stock Table        ║
║  ──────────────────────     │  ─────────────────  ║
║  □ Risk Profile:            │  [Search box]       ║
║    ☑ Low Risk               │                     ║
║    ☑ Medium-Low             │  Stock  Sector Risk ║
║    ☐ Medium-High            │  ───── ────── ───── ║
║    ☐ High Risk              │  SCOM  Telecom  Med │
║                             │  KCB   Banking  Low │
║  □ Sector:                  │  ABSA  Banking  Low │
║    ☑ Banking                │  ...               │
║    ☑ Telecom                │                     ║
║    ☐ Manufacturing          │  [Showing 25 of 57] ║
║                             │                     ║
║  □ Metrics:                 │  ─────────────────  ║
║    Volatility: [slider]     │  Click row for      ║
║    Sharpe: [slider]         │  detailed view →    ║
╚═══════════════════════════════════════════════════╝
```

---

### Page 3: Predictions (Upload New Data)

**Features:**
- Upload new stock CSV
- Predict risk profile
- Show confidence scores
- Downloadable results

**UI Mockup:**
```
╔═══════════════════════════════════════════════════╗
║  🔮 PREDICT RISK PROFILE FOR NEW STOCKS           ║
╠═══════════════════════════════════════════════════╣
║                                                   ║
║  📁 Upload Stock Data:                            ║
║  ┌─────────────────────────────────────────────┐ ║
║  │  [Browse...]  new_stocks.csv                │ ║
║  │                                              │ ║
║  │  Required columns:                           │ ║
║  │  - Date, Stock_code, Day Price, Volume, ... │ ║
║  └─────────────────────────────────────────────┘ ║
║                                                   ║
║  [Predict Risk Profile] ← Button                 ║
║                                                   ║
║  📊 Results:                                      ║
║  ┌─────────────────────────────────────────────┐ ║
║  │ Stock XYZ                                    │ ║
║  │ Predicted Risk: Medium-High                  │ ║
║  │ Confidence: 85%                              │ ║
║  │                                              │ ║
║  │ Key Features:                                │ ║
║  │ - Volatility: High (3.2%)                    │ ║
║  │ - Sharpe Ratio: 0.6                          │ ║
║  │ - Max Drawdown: -25%                         │ ║
║  └─────────────────────────────────────────────┘ ║
║                                                   ║
║  [Download Results CSV]                          ║
╚═══════════════════════════════════════════════════╝
```

---

## 12.3 Code Implementation

### Full `app.py` (Production-Ready)

```python
# ============================================
# IMPORTS
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.clustering import StockClusterer
from src.features import *

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="NSE Stock Risk Analyzer",
    page_icon="📊",
    layout="wide",  # Use full width
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS (Make it Pretty!)
# ============================================

st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .risk-low { color: #2ecc71; }
    .risk-medium-low { color: #f39c12; }
    .risk-medium-high { color: #e67e22; }
    .risk-high { color: #e74c3c; }
    </style>
""", unsafe_allow_html=True)

# ============================================
# DATA LOADING (CACHED!)
# ============================================

@st.cache_data
def load_clustered_data():
    """Load pre-clustered stock data."""
    df = pd.read_csv("Data/Processed/nse_clustered.csv")
    return df

@st.cache_resource
def load_model():
    """Load trained clustering model."""
    model = StockClusterer.load_model("models/stock_clusterer.pkl")
    return model

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_risk_color(risk_profile):
    """Return color for risk category."""
    colors = {
        "Low Risk": "#2ecc71",
        "Medium-Low Risk": "#f39c12",
        "Medium-High Risk": "#e67e22",
        "High Risk": "#e74c3c"
    }
    return colors.get(risk_profile, "#95a5a6")

def create_risk_distribution_chart(df):
    """Create pie chart of risk distribution."""
    risk_counts = df['Risk_Profile'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=risk_counts.index,
        values=risk_counts.values,
        hole=0.4,  # Donut chart
        marker=dict(colors=[get_risk_color(r) for r in risk_counts.index])
    )])
    
    fig.update_layout(
        title="Risk Profile Distribution",
        height=400
    )
    
    return fig

def create_sector_chart(df):
    """Create bar chart of stocks per sector."""
    sector_risk = df.groupby(['Sector', 'Risk_Profile']).size().reset_index(name='count')
    
    fig = px.bar(
        sector_risk,
        x='Sector',
        y='count',
        color='Risk_Profile',
        title="Stocks by Sector and Risk",
        color_discrete_map={
            "Low Risk": "#2ecc71",
            "Medium-Low Risk": "#f39c12",
            "Medium-High Risk": "#e67e22",
            "High Risk": "#e74c3c"
        }
    )
    
    fig.update_layout(height=400)
    return fig

def create_scatter_plot(df):
    """Create interactive scatter: volatility vs return."""
    fig = px.scatter(
        df,
        x='volatility_mean',
        y='mean_return',
        color='Risk_Profile',
        size='avg_volume',
        hover_data=['Stock_code', 'Name', 'sharpe_ratio'],
        title="Risk-Return Profile",
        labels={
            'volatility_mean': 'Volatility (Risk)',
            'mean_return': 'Average Return'
        },
        color_discrete_map={
            "Low Risk": "#2ecc71",
            "Medium-Low Risk": "#f39c12",
            "Medium-High Risk": "#e67e22",
            "High Risk": "#e74c3c"
        }
    )
    
    fig.update_layout(height=500)
    return fig

# ============================================
# MAIN APP
# ============================================

def main():
    # Header
    st.markdown('<div class="main-header">📊 NSE Stock Risk Analyzer</div>', 
                unsafe_allow_html=True)
    st.markdown("### Intelligent Stock Clustering for Smart Investing")
    
    # Load data
    with st.spinner("Loading data..."):
        df = load_clustered_data()
        model = load_model()
    
    # Sidebar filters
    with st.sidebar:
        st.header("🎛️ Filters")
        
        # Risk filter
        risk_options = st.multiselect(
            "Risk Profile:",
            options=df['Risk_Profile'].unique(),
            default=df['Risk_Profile'].unique()
        )
        
        # Sector filter
        sector_options = st.multiselect(
            "Sector:",
            options=df['Sector'].unique(),
            default=df['Sector'].unique()
        )
        
        # Metric filters
        st.subheader("Metric Ranges")
        
        vol_range = st.slider(
            "Volatility:",
            float(df['volatility_mean'].min()),
            float(df['volatility_mean'].max()),
            (float(df['volatility_mean'].min()), float(df['volatility_mean'].max()))
        )
        
        sharpe_range = st.slider(
            "Sharpe Ratio:",
            float(df['sharpe_ratio'].min()),
            float(df['sharpe_ratio'].max()),
            (float(df['sharpe_ratio'].min()), float(df['sharpe_ratio'].max()))
        )
    
    # Apply filters
    filtered_df = df[
        (df['Risk_Profile'].isin(risk_options)) &
        (df['Sector'].isin(sector_options)) &
        (df['volatility_mean'].between(vol_range[0], vol_range[1])) &
        (df['sharpe_ratio'].between(sharpe_range[0], sharpe_range[1]))
    ]
    
    # ============================================
    # SECTION 1: KEY METRICS
    # ============================================
    
    st.header("📈 Portfolio Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Stocks",
            len(filtered_df),
            delta=f"{len(filtered_df) - len(df)} from filter"
        )
    
    with col2:
        avg_return = filtered_df['mean_return'].mean()
        st.metric(
            "Avg Daily Return",
            f"{avg_return:.4f}%",
            delta=f"{(avg_return - df['mean_return'].mean()):.4f}%"
        )
    
    with col3:
        avg_sharpe = filtered_df['sharpe_ratio'].mean()
        st.metric(
            "Avg Sharpe Ratio",
            f"{avg_sharpe:.2f}",
            delta=f"{(avg_sharpe - df['sharpe_ratio'].mean()):.2f}"
        )
    
    with col4:
        avg_vol = filtered_df['volatility_mean'].mean()
        st.metric(
            "Avg Volatility",
            f"{avg_vol:.4f}%",
            delta=f"{(avg_vol - df['volatility_mean'].mean()):.4f}%",
            delta_color="inverse"  # Lower is better for volatility
        )
    
    # ============================================
    # SECTION 2: VISUALIZATIONS
    # ============================================
    
    st.header("📊 Visual Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_risk_distribution_chart(filtered_df), 
                        use_container_width=True)
    
    with col2:
        st.plotly_chart(create_sector_chart(filtered_df), 
                        use_container_width=True)
    
    st.plotly_chart(create_scatter_plot(filtered_df), 
                    use_container_width=True)
    
    # ============================================
    # SECTION 3: TOP STOCKS
    # ============================================
    
    st.header("🏆 Top Stocks by Risk Category")
    
    tabs = st.tabs(["Low Risk", "Medium-Low", "Medium-High", "High Risk"])
    
    for i, risk in enumerate(["Low Risk", "Medium-Low Risk", "Medium-High Risk", "High Risk"]):
        with tabs[i]:
            risk_stocks = filtered_df[filtered_df['Risk_Profile'] == risk].nlargest(5, 'sharpe_ratio')
            
            if len(risk_stocks) == 0:
                st.info("No stocks in this category (filtered out)")
            else:
                st.dataframe(
                    risk_stocks[['Stock_code', 'Name', 'Sector', 'sharpe_ratio', 
                                'mean_return', 'volatility_mean', 'max_drawdown']],
                    use_container_width=True
                )
    
    # ============================================
    # SECTION 4: STOCK EXPLORER
    # ============================================
    
    st.header("🔍 Stock Explorer")
    
    search = st.text_input("Search stocks (by code or name):")
    
    if search:
        search_df = filtered_df[
            filtered_df['Stock_code'].str.contains(search, case=False, na=False) |
            filtered_df['Name'].str.contains(search, case=False, na=False)
        ]
    else:
        search_df = filtered_df
    
    st.dataframe(search_df, use_container_width=True)
    
    # ============================================
    # SECTION 5: PREDICTION (NEW STOCKS)
    # ============================================
    
    st.header("🔮 Predict Risk for New Stock")
    
    with st.expander("Upload new stock data"):
        uploaded_file = st.file_uploader("Choose CSV file", type=['csv'])
        
        if uploaded_file is not None:
            new_df = pd.read_csv(uploaded_file)
            
            st.success(f"Loaded {len(new_df)} rows")
            st.dataframe(new_df.head())
            
            if st.button("Calculate Features & Predict"):
                with st.spinner("Processing..."):
                    # Feature engineering (call functions from src/features.py)
                    new_df = calculate_returns(new_df)
                    new_df = calculate_volatility_features(new_df)
                    new_df = calculate_risk_metrics(new_df)
                    new_df = calculate_technical_indicators(new_df)
                    new_df = calculate_liquidity_features(new_df)
                    new_df = calculate_momentum_features(new_df)
                    new_df = calculate_drawdown(new_df)
                    
                    # Aggregate
                    features_list = []
                    for stock in new_df['Stock_code'].unique():
                        stock_data = new_df[new_df['Stock_code'] == stock]
                        features = aggregate_stock_features(stock_data)
                        if features:
                            features_list.append(features)
                    
                    features_df = pd.DataFrame(features_list)
                    
                    # Predict
                    predictions = model.predict(features_df)
                    features_df['Predicted_Risk'] = predictions
                    
                    st.success("✅ Prediction complete!")
                    st.dataframe(features_df[['Stock_code', 'Name', 'Predicted_Risk', 
                                              'sharpe_ratio', 'volatility_mean']])
                    
                    # Download button
                    csv = features_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results",
                        data=csv,
                        file_name="predicted_risks.csv",
                        mime="text/csv"
                    )

# ============================================
# RUN APP
# ============================================

if __name__ == "__main__":
    main()
```

---

## 12.4 Requirements File

Create `requirements.txt` for deployment:

```txt
streamlit==1.31.0
pandas==2.1.4
numpy==1.26.3
scikit-learn==1.4.0
plotly==5.18.0
scipy==1.12.0
```

---

## 12.5 Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py

# App opens at: http://localhost:8501
```

---

# Chapter 13: Deployment

## 13.1 Streamlit Cloud (Free Hosting!)

### Step 1: Push to GitHub
```bash
cd /home/user/webapp
git add app.py requirements.txt
git commit -m "Add Streamlit app"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. **Go to:** https://streamlit.io/cloud
2. **Sign in** with GitHub
3. **Click "New app"**
4. **Select:**
   - Repository: `yourusername/stocks`
   - Branch: `main`
   - Main file: `app.py`
5. **Click "Deploy"**

**Done!** App is live at: `https://yourusername-stocks-app.streamlit.app`

### Step 3: Share with World
- Get permanent URL
- Anyone can access (no login needed)
- Auto-updates when you push to GitHub

---

## 13.2 Advanced: Custom Domain

**Streamlit Cloud Pro ($):**
- Custom domain (e.g., `stockanalyzer.com`)
- Password protection
- More resources (memory, CPU)

**Alternative (Free):**
- Deploy on Heroku/Railway/Render
- Use free domain from Freenom
- More setup but fully customizable

---

## 13.3 Performance Optimization

### Tip 1: Cache Everything
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    return pd.read_csv("data.csv")
```

### Tip 2: Lazy Loading
```python
# Don't load all data at once
if st.button("Show detailed analysis"):
    # Only compute when clicked
    run_expensive_analysis()
```

### Tip 3: Pagination
```python
# Show 10 stocks per page
page = st.number_input("Page", 1, 10)
start = (page - 1) * 10
end = start + 10
st.dataframe(df.iloc[start:end])
```

### Tip 4: Async Loading
```python
with st.spinner("Loading..."):
    df = load_data()  # Shows spinner while loading
st.success("Loaded!")
```

---

# Chapter 14: Advanced Features (Optional)

## 14.1 Real-Time Data Integration

**Use Alpha Vantage API (Free):**
```python
import requests
import streamlit as st

@st.cache_data(ttl=300)  # Refresh every 5 minutes
def get_live_price(symbol):
    API_KEY = st.secrets["ALPHAVANTAGE_KEY"]  # Store in Streamlit secrets
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return float(data['Global Quote']['05. price'])

# Usage
live_price = get_live_price("SCOM")
st.metric("Safaricom Live Price", f"KES {live_price:.2f}")
```

---

## 14.2 User Authentication

**Using `streamlit-authenticator`:**
```python
import streamlit as st
import streamlit_authenticator as stauth

# Define users
names = ['John Doe', 'Jane Smith']
usernames = ['jdoe', 'jsmith']
passwords = ['abc123', 'def456']

# Hash passwords
hashed_passwords = stauth.Hasher(passwords).generate()

# Create authenticator
authenticator = stauth.Authenticate(
    names, usernames, hashed_passwords,
    'stock_app', 'secret_key', cookie_expiry_days=30
)

# Login widget
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'sidebar')
    st.write(f'Welcome *{name}*!')
    # Your app code here
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
```

---

## 14.3 Database Integration (Store User Portfolios)

**Using SQLite:**
```python
import sqlite3
import streamlit as st

def init_db():
    conn = sqlite3.connect('portfolios.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS portfolios
        (user TEXT, stock TEXT, quantity INTEGER, price REAL)
    ''')
    conn.commit()
    conn.close()

def save_portfolio(user, stock, quantity, price):
    conn = sqlite3.connect('portfolios.db')
    c = conn.cursor()
    c.execute('INSERT INTO portfolios VALUES (?, ?, ?, ?)',
              (user, stock, quantity, price))
    conn.commit()
    conn.close()

def get_portfolio(user):
    conn = sqlite3.connect('portfolios.db')
    df = pd.read_sql(f'SELECT * FROM portfolios WHERE user="{user}"', conn)
    conn.close()
    return df

# Usage
init_db()
if st.button("Save to Portfolio"):
    save_portfolio('jdoe', 'SCOM', 100, 25.50)
    st.success("Saved!")

portfolio = get_portfolio('jdoe')
st.dataframe(portfolio)
```

---

## 14.4 Email Alerts

**Using `smtplib`:**
```python
import smtplib
from email.mime.text import MIMEText

def send_alert(to_email, stock, price):
    msg = MIMEText(f"Stock {stock} reached target price: {price}")
    msg['Subject'] = 'Stock Alert!'
    msg['From'] = 'alerts@stockapp.com'
    msg['To'] = to_email
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('your_email@gmail.com', 'your_password')
        server.send_message(msg)

# Usage in app
if stock_price > target_price:
    send_alert(user_email, stock, stock_price)
    st.success("Alert sent to your email!")
```

---

# Chapter 15: Presentation & Demo Tips

## 15.1 Demo Script

**Opening (30 seconds):**
> "Hi! Today I'm presenting my NSE Stock Clustering project. I built an intelligent system that groups 57 Kenyan stocks into risk categories using machine learning. Let me show you."

**Live Demo (2 minutes):**

1. **Open app** (have it running beforehand!)
   - Point out clean UI
   
2. **Show dashboard:**
   - "Here we see 57 stocks, average Sharpe ratio 0.8, silhouette score 0.52"
   - "This pie chart shows risk distribution"

3. **Interact with filters:**
   - "I can filter by risk - let me show only High Risk stocks"
   - "Or filter by sector - only Banking stocks"

4. **Click on stock:**
   - "Click any stock to see details"
   - "Safaricom: Medium-Low Risk, Sharpe 0.9, volatility 2.1%"

5. **Upload prediction:**
   - "I can upload new stock data and predict its risk"
   - Upload pre-prepared CSV
   - "Model predicts: Medium-High Risk with 85% confidence"

**Technical Explanation (2 minutes):**
- Feature engineering (Sharpe, RSI, Bollinger Bands)
- K-Means clustering with RobustScaler
- Silhouette score improved from 0.32 to 0.52
- 15 carefully selected features

**Business Value (1 minute):**
- Helps investors choose stocks matching risk tolerance
- Saves hours of manual analysis
- Data-driven, removes emotional bias

**Q&A (remaining time)**

---

## 15.2 Common Questions & Answers

**Q: Why K-Means instead of other algorithms?**
> A: K-Means is fast, interpretable, and works well for spherical clusters. Our financial features form natural risk tiers, making K-Means ideal. I also tested Hierarchical Clustering but K-Means gave better Silhouette scores.

**Q: How did you choose 15 features?**
> A: Started with 25 features from literature review (volatility, Sharpe, RSI, etc.). Tested different combinations. 15 features balanced information vs. curse of dimensionality. More features degraded Silhouette score.

**Q: Can this predict future stock performance?**
> A: No, it classifies RISK level (volatility, drawdown), not future returns. It helps investors pick stocks matching their risk tolerance, not "get rich quick."

**Q: How often should model be retrained?**
> A: Quarterly. Stock characteristics change with market conditions. I'd automate retraining with new data every 3 months.

**Q: What if market crashes?**
> A: Model based on historical volatility. In crash, all stocks become "High Risk." Model should be used with market context, not in isolation.

**Q: Why RobustScaler over StandardScaler?**
> A: Financial data has outliers (market crashes, booms). RobustScaler uses median and IQR, robust to extremes. StandardScaler would let outliers distort scaling.

**Q: How does this compare to industry tools (Bloomberg, FactSet)?**
> A: Those are comprehensive (fundamentals, news, analyst ratings). My project focuses on technical risk clustering, complementary to those tools. Mine is open-source and customizable.

---

## 15.3 Portfolio Value-Add

**Showcase These Skills:**

**Technical:**
- ✅ Machine Learning (K-Means, evaluation metrics)
- ✅ Feature Engineering (15+ financial indicators)
- ✅ Data Processing (pandas, numpy)
- ✅ Visualization (Plotly, Streamlit)
- ✅ Software Engineering (modular code, version control)
- ✅ Deployment (Streamlit Cloud)

**Domain:**
- ✅ Financial Markets (stocks, risk, returns)
- ✅ Portfolio Management (risk-adjusted performance)
- ✅ Technical Analysis (RSI, MACD, Bollinger Bands)

**Soft Skills:**
- ✅ Problem Solving (improved Silhouette 0.32 → 0.52)
- ✅ Communication (dashboard for non-technical users)
- ✅ Business Acumen (practical investor tool)

**GitHub README Highlights:**
```markdown
## 🎯 Key Achievements
- Achieved Silhouette Score 0.52 (excellent cluster separation)
- Engineered 15+ advanced financial features
- Built interactive Streamlit dashboard
- Deployed live: [stockanalyzer.streamlit.app](https://...)

## 💡 What I Learned
- Feature engineering is more impactful than algorithm choice
- RobustScaler critical for financial data (outliers!)
- Domain knowledge drives feature selection
- Visualizations bridge technical ↔ business

## 🚀 Future Enhancements
- Real-time data integration (Alpha Vantage API)
- Fundamental analysis features (P/E ratio, debt)
- Portfolio optimization (efficient frontier)
- User authentication & saved portfolios
```

---

# Final Checklist Before Presentation

## ✅ Technical
- [ ] All notebooks run without errors
- [ ] Silhouette score ≥ 0.5
- [ ] Model saved in `models/` folder
- [ ] Streamlit app runs locally
- [ ] App deployed on Streamlit Cloud
- [ ] GitHub README updated
- [ ] Requirements.txt complete

## ✅ Documentation
- [ ] Read this guide (all chapters!)
- [ ] Understand every line of `features.py`
- [ ] Understand every line of `clustering.py`
- [ ] Can explain each feature (Sharpe, RSI, etc.)
- [ ] Can explain why RobustScaler
- [ ] Can explain K=4 choice

## ✅ Presentation
- [ ] Prepare 5-minute demo script
- [ ] Practice demo (time yourself!)
- [ ] Prepare answers to common questions
- [ ] Have backup slides (if demo fails)
- [ ] Test screen sharing (if remote)

## ✅ Portfolio
- [ ] GitHub repo is public
- [ ] Clean commit history
- [ ] Professional README
- [ ] Add to LinkedIn/resume
- [ ] Prepare 2-minute elevator pitch

---

**YOU'RE NOW A PRO!** 🎉

You understand:
- ✅ Machine learning theory (clustering, evaluation)
- ✅ Financial concepts (risk, return, Sharpe, drawdown)
- ✅ Technical indicators (RSI, MACD, Bollinger Bands)
- ✅ Every line of your code
- ✅ How to build and deploy a Streamlit app
- ✅ How to present your project professionally

**Next Steps:**
1. Re-read this guide (take notes!)
2. Explain concepts out loud (to a friend or mirror)
3. Modify app (add your own feature)
4. Deploy and share
5. Use this as stepping stone for next project!

**You got this!** 💪

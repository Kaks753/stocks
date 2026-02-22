# 📚 NSE STOCK CLUSTERING: COMPLETE MASTERY GUIDE
## From Beginner to Professional Data Scientist

**Author:** Your AI Mentor  
**Purpose:** Transform you into a confident expert who understands EVERY concept, EVERY line of code, and EVERY decision  
**Time to Master:** Read carefully, take notes, practice explaining concepts out loud

---

# 🌟 PART 1: FOUNDATIONAL CONCEPTS

## Chapter 1: Machine Learning Fundamentals

### 1.1 What is Machine Learning?

**Simple Definition:**  
Machine Learning is teaching computers to learn patterns from data without explicitly programming rules.

**Real-World Analogy:**
- **Traditional Programming:** "If price > 100, then classify as expensive"
- **Machine Learning:** Show computer 1000 examples of expensive/cheap items, it learns the pattern itself

**Three Types of Machine Learning:**

#### 1. Supervised Learning (Teacher Present)
- **What:** You have input data AND correct answers (labels)
- **Example:** Email spam detection
  - Input: Email text
  - Label: Spam or Not Spam
  - Algorithm learns: "Emails with words like 'winner', 'free money' are spam"
- **Common Algorithms:** Linear Regression, Decision Trees, Neural Networks

#### 2. Unsupervised Learning (No Teacher) ⭐ **WE USE THIS**
- **What:** You have input data but NO labels - algorithm finds hidden patterns
- **Example:** Customer segmentation
  - Input: Customer purchase history
  - No labels (we don't know groups beforehand)
  - Algorithm discovers: "Group 1 = luxury buyers, Group 2 = budget shoppers"
- **Common Algorithms:** K-Means Clustering, Hierarchical Clustering, PCA

#### 3. Reinforcement Learning (Learning by Trial & Error)
- **What:** Agent learns by receiving rewards/penalties
- **Example:** Training AI to play chess
- **Not used in our project**

**Why We Use Unsupervised Learning:**
- NSE stocks don't come with risk labels ("Low Risk", "High Risk")
- We want algorithm to DISCOVER natural groupings based on financial behavior
- No human bias - purely data-driven

---

## Chapter 2: Clustering - The Complete Theory

### 2.1 What is Clustering?

**Definition:**  
Clustering is grouping similar items together based on their characteristics.

**Real-World Examples:**

1. **Netflix Movie Recommendations:**
   - Groups movies by genre, mood, audience
   - "People who watched Action movies also liked these..."

2. **Customer Segmentation:**
   - Retail stores group customers: VIP, Regular, Occasional
   - Each group gets different marketing

3. **Image Compression:**
   - Group similar colors together
   - Reduce file size while maintaining quality

4. **Our Project - Stock Risk Grouping:**
   - Group stocks by volatility, returns, liquidity
   - Investors pick groups matching their risk tolerance

**Key Concept - Similarity:**
- Clustering relies on measuring "how similar" two items are
- For stocks: similar volatility, similar returns = similar risk

---

### 2.2 Types of Clustering Algorithms

#### A. K-Means Clustering ⭐ **WE USE THIS**

**How It Works (Simple Explanation):**

1. **Step 1 - Random Centers:** Pick K random points as cluster "centers"
2. **Step 2 - Assign:** Each stock joins the nearest center
3. **Step 3 - Update:** Move each center to the average position of its members
4. **Step 4 - Repeat:** Keep assigning and updating until centers stop moving

**Visual Analogy:**
Imagine 4 teachers in a playground. Students run to the nearest teacher. Teachers then move to the center of their student group. Repeat until groups stabilize.

**Advantages:**
- ✅ Fast (works on millions of data points)
- ✅ Simple to understand
- ✅ Works well when clusters are roughly circular/spherical
- ✅ Scales to large datasets

**Disadvantages:**
- ❌ Must choose K (number of clusters) beforehand
- ❌ Sensitive to outliers (extreme values)
- ❌ Assumes clusters are spherical (not good for weird shapes)
- ❌ Random initialization can give different results

**Why We Chose K-Means:**
- Financial data tends to form natural risk tiers (Low, Medium, High)
- We have 57 stocks - K-Means handles this easily
- Need fast results for presentation
- Clusters ARE roughly spherical in our feature space

---

#### B. Hierarchical Clustering (Alternative Method)

**How It Works:**
- Build a tree (dendrogram) of clusters
- Start: each point is its own cluster
- Merge closest clusters step-by-step
- End: all points in one giant cluster

**When to Use:**
- Want to see relationships at multiple levels
- Don't know K beforehand
- Have small dataset (<1000 points)

**Why We DIDN'T Use It:**
- Slower than K-Means (O(n³) complexity)
- Less interpretable for business users
- K-Means sufficient for our needs

---

#### C. DBSCAN (Density-Based Clustering)

**How It Works:**
- Finds regions where points are densely packed
- Can detect irregular cluster shapes
- Automatically identifies outliers

**When to Use:**
- Clusters have weird shapes (crescents, spirals)
- Need to detect anomalies/outliers
- Don't want to force all points into clusters

**Why We DIDN'T Use It:**
- Our clusters are roughly spherical
- K-Means simpler for stakeholders to understand
- We want ALL stocks assigned (no outliers)

---

### 2.3 How to Choose Number of Clusters (K)

This is THE most important decision in clustering!

#### Method 1: Elbow Method ⭐ **WE USE THIS**

**Concept:**
- Plot "inertia" (how spread out clusters are) vs. K
- Look for the "elbow" - point where adding clusters doesn't help much

**Example:**
```
K=2: Inertia = 1000  (too few clusters, points spread out)
K=3: Inertia = 500   (better)
K=4: Inertia = 300   (elbow here! ✓)
K=5: Inertia = 280   (small improvement)
K=6: Inertia = 270   (diminishing returns)
```

**Visual:**
```
Inertia
   |
1000|●
    |
 500|  ●
    |    ●  ← Elbow (choose K=4)
 300|      ●___●___●
    +--+--+--+--+--+--→ K
       2  3  4  5  6
```

**Our Decision:**
- K=4 gives us: Low Risk, Medium-Low, Medium-High, High Risk
- Business-friendly (matches risk tolerance categories)
- Elbow appears around K=4

---

#### Method 2: Silhouette Score ⭐ **WE USE THIS**

**What It Measures:**
- How well-separated clusters are
- Score from -1 to +1
  - **+1:** Perfect (clusters far apart, tightly packed within)
  - **0:** Overlapping clusters
  - **-1:** Wrong clustering (points in wrong clusters)

**Interpretation:**
```
Score > 0.7  → Excellent (strong natural structure)
Score 0.5-0.7 → Good (clear clusters) ✓ OUR TARGET
Score 0.3-0.5 → Moderate (some overlap)
Score < 0.3  → Poor (forced clustering)
```

**Why This Matters:**
- Validates that our clusters are REAL, not random
- Score of 0.5+ means investors can trust the groupings
- Lower score = stocks might be in wrong risk categories

---

#### Method 3: Business Logic

**Sometimes domain knowledge beats algorithms!**

**For Stock Risk:**
- Investors understand 4 risk levels (Low, Med-Low, Med-High, High)
- Too few (K=2): "Low vs High" too simplistic
- Too many (K=7): Confusing, hard to choose
- K=4: Just right - matches investment industry standards

**Our Final Choice:**
```python
n_clusters = 4
```
**Reason:** Best balance of statistical quality + business interpretability

---

### 2.4 Evaluating Cluster Quality

#### A. Inertia (Within-Cluster Sum of Squares)

**Formula:**
```
Inertia = Σ (distance from each point to its cluster center)²
```

**Interpretation:**
- Lower = better (points close to centers)
- BUT: Always decreases as K increases
- Need other metrics too!

**Our Use:**
- Plot elbow curve
- Not used alone for evaluation

---

#### B. Silhouette Score (Primary Metric) ⭐

**Formula (for one point i):**
```
a = average distance to points in same cluster
b = average distance to points in nearest other cluster

Silhouette(i) = (b - a) / max(a, b)
```

**Intuition:**
- **a small:** Point is close to cluster-mates (good!)
- **b large:** Point is far from other clusters (good!)
- **Score high:** Both conditions met = well-clustered

**Our Threshold:**
```python
if silhouette >= 0.5:
    print("Excellent clustering!")
```

---

#### C. Visual Inspection (Sanity Check)

**Always check:**
1. **PCA Plot:** Clusters visually separated?
2. **Cluster Sizes:** Any cluster with only 1-2 stocks? (bad)
3. **Feature Distributions:** Do clusters have distinct characteristics?

**Red Flags:**
- One huge cluster + tiny clusters → Poor K choice
- Overlapping clusters in PCA → Low Silhouette
- All clusters look similar → Not useful for investors

---

## Chapter 3: Financial Markets & Stock Analysis

### 3.1 What is a Stock?

**Simple Definition:**  
A stock is a small piece of ownership in a company.

**Real-World Analogy:**
- Company = Pizza
- Stock = One slice
- You buy slices, you own part of the pizza!

**Why Stocks Have Prices:**
- Price = what people willing to pay
- Goes up when: company doing well, demand high
- Goes down when: bad news, people selling

**NSE (Nairobi Securities Exchange):**
- Kenya's stock market
- Where Kenyan companies trade (Safaricom, ABSA, KCB, etc.)
- Our project: 57 NSE stocks from 2021-2023

---

### 3.2 Key Stock Metrics (Column Names Explained)

#### Price Columns

**1. Day Price (Close Price)**
```python
df['Day Price']
```
- **What:** Final price when market closed that day
- **Real Life:** Like checking product price at store closing time
- **Why Important:** Most commonly used price for analysis
- **Example:** Safaricom closed at KES 25.50 on Jan 5, 2024

**2. Day Low / Day High**
```python
df['Day Low'], df['Day High']
```
- **What:** Lowest/highest price during trading day
- **Real Life:** Like "item ranged from $10-$15 today"
- **Why Important:** Shows daily volatility (price swings)
- **Example:** If Day High - Day Low is large = very volatile stock

**3. 12m Low / 12m High**
```python
df['12m Low'], df['12m High']
```
- **What:** Lowest/highest price in past 12 months
- **Real Life:** "This product was cheapest at $5, most expensive at $50 this year"
- **Why Important:** Shows long-term range, helps identify if stock is near peak or bottom
- **Example:** Stock near 12m High = might be overvalued

**4. Previous (Previous Close)**
```python
df['Previous']
```
- **What:** Yesterday's closing price
- **Why Important:** Compare to today's price to see daily change
- **Example:** Previous = 100, Today = 105 → +5% gain

**5. Adjusted Price**
```python
df['Adjusted Price']
```
- **What:** Price adjusted for corporate actions (stock splits, dividends)
- **Real Life:** Like adjusting pizza price when they change slice size
- **Why Important:** Accurate historical comparison
- **Example:** Company does 2-for-1 split, price halves but you own 2x shares

---

#### Change Columns

**6. Change**
```python
df['Change']
```
- **Formula:** `Change = Day Price - Previous`
- **Example:** Previous = 100, Today = 105 → Change = +5
- **Interpretation:** Absolute price movement

**7. %Change (Percentage Change)**
```python
df['%Change']
```
- **Formula:** `%Change = (Day Price - Previous) / Previous * 100`
- **Example:** Previous = 100, Today = 105 → %Change = +5%
- **Why Better Than Change:** Fair comparison across stocks
  - Stock A: $10 → $11 = +$1 (10% gain)
  - Stock B: $100 → $101 = +$1 (1% gain)
  - Same change, different impact!

---

#### Trading Columns

**8. Volume**
```python
df['Volume']
```
- **What:** Number of shares traded that day
- **Real Life:** Like "100 customers bought this product today"
- **Why Important:** Shows liquidity (how easy to buy/sell)
- **High Volume:** Easy to trade, popular stock
- **Low Volume:** Hard to sell, risky (you might be stuck!)
- **Example:** Safaricom volume = 10M shares, small company = 1K shares

---

#### Categorical Columns

**9. Stock_code**
```python
df['Stock_code']
```
- **What:** Unique identifier (ticker symbol)
- **Example:** "SCOM" = Safaricom, "KCB" = KCB Bank
- **Why Important:** Used to track/group data by company

**10. Name**
```python
df['Name']
```
- **What:** Full company name
- **Example:** "Safaricom PLC"

**11. Sector**
```python
df['Sector']
```
- **What:** Industry category
- **Examples:**
  - Banking: KCB, Equity, ABSA
  - Telecommunications: Safaricom
  - Manufacturing: EABL (East African Breweries)
- **Why Important:** Stocks in same sector behave similarly
  - All banks affected by interest rate changes
  - All manufacturers affected by oil prices

---

#### Date Columns

**12. Date**
```python
df['Date']
```
- **Format:** YYYY-MM-DD (2021-01-04)
- **Why Important:** Sort data chronologically, calculate time-based features

**13. Month, Year**
```python
df['Month'], df['Year']
```
- **Derived from Date:** For grouping and analysis
- **Example Use:** "Show average return per month"

---

### 3.3 Return vs. Price (Critical Concept!)

**Why We Use Returns, Not Prices:**

**Problem with Prices:**
- Stock A: $10 → $11 = +$1
- Stock B: $100 → $101 = +$1
- Same change, but Stock A gained 10%, Stock B only 1%!

**Solution: Calculate Returns (% Change)**
```python
return = (price_today - price_yesterday) / price_yesterday
```

**Example:**
```python
# Stock A
return_A = (11 - 10) / 10 = 0.10 = 10%

# Stock B
return_B = (101 - 100) / 100 = 0.01 = 1%
```

**Now comparable!** Stock A performed better.

**Types of Returns:**

**1. Simple Return (Arithmetic)**
```python
return = (P_t - P_{t-1}) / P_{t-1}
```
- Easy to understand
- **Problem:** Not additive over time
  - +50% then -50% ≠ 0% (you lose money!)
  - Day 1: $100 → $150 (+50%)
  - Day 2: $150 → $75 (-50%)
  - Total: $100 → $75 = -25% loss, not 0%!

**2. Log Return (We use this!) ⭐**
```python
log_return = ln(P_t / P_{t-1})
```
- **Advantage:** Additive over time
  - Sum of daily log returns = total return
- **Advantage:** Symmetric (easier math)
- **Used in finance research**

**Our Code:**
```python
df['daily_return'] = df.groupby('Stock_code')['Day Price'].pct_change()
df['log_return'] = np.log(df['Day Price'] / df['Previous'])
```

---

### 3.4 Risk in Finance

**What is Risk?**  
Risk = Uncertainty about future returns

**Two Types:**

#### 1. Volatility (How Much Price Swings)
- **High Volatility:** Price jumps $10, $15, $20 daily (scary!)
- **Low Volatility:** Price changes $1, $2 daily (boring but safe)
- **Measured by:** Standard deviation of returns

**Example:**
- Stock A: Returns = [1%, 2%, 1.5%, 1.8%] → Low volatility (predictable)
- Stock B: Returns = [-10%, +20%, -5%, +15%] → High volatility (risky!)

---

#### 2. Drawdown (How Much You Lose from Peak)
- **What:** Maximum loss from highest point
- **Example:**
  - Stock peaks at $100
  - Drops to $70
  - Drawdown = -30%
- **Why Scary:** Shows worst-case scenario
  - 50% drawdown means you lost HALF your money!

---

**Risk-Return Tradeoff:**
```
High Risk → High Potential Return (but might lose a lot!)
Low Risk → Low Return (but you sleep well at night)
```

**Investor Types:**
- **Aggressive:** Young, can handle losses → High risk stocks
- **Conservative:** Near retirement → Low risk stocks
- **Our Project Goal:** Group stocks by risk so investors pick their level!

---

## Chapter 4: Feature Engineering for Finance

### 4.1 What is a Feature?

**Definition:**  
A feature is a measurable property used for prediction or grouping.

**Real-World Examples:**

**Predicting House Prices:**
- Features: Square footage, bedrooms, location, age
- Algorithm learns: "Big houses in good areas cost more"

**Email Spam Detection:**
- Features: Word count, sender domain, links present
- Algorithm learns: "Many links + unknown sender = spam"

**Our Stock Clustering:**
- Features: Volatility, returns, momentum, liquidity
- Algorithm learns: "High volatility + low liquidity = high risk"

---

### 4.2 Why Feature Engineering Matters

**Story:**  
Imagine classifying fruits with only "color" as feature:
- Apple (red), Tomato (red) → Algorithm confuses them!

Add "sweetness" feature:
- Apple (red, sweet), Tomato (red, savory) → Now distinguishable!

**In Our Project:**

**Bad Features (Attempt 1):**
- Only volatility, returns → Silhouette = 0.18 (poor!)
- Many stocks looked similar

**Good Features (Final):**
- Volatility, Sharpe ratio, RSI, drawdown, liquidity → Silhouette = 0.5+ (excellent!)
- Clear risk separation

**Key Lesson:**  
*Better features > fancier algorithms*

---

### 4.3 Types of Features

#### A. Raw Features (Direct from Data)
```python
df['Day Price']      # Price itself
df['Volume']         # Trading volume
df['%Change']        # Daily % change
```
- **Pros:** Easy to get
- **Cons:** Not always useful (prices not comparable across stocks)

#### B. Derived Features (Calculated) ⭐ **WE CREATE THESE**
```python
# Return (% change)
return = (price_today - price_yesterday) / price_yesterday

# Volatility (standard deviation of returns)
volatility = std(returns)

# Sharpe Ratio (risk-adjusted return)
sharpe = mean(returns) / std(returns)
```
- **Pros:** Capture hidden patterns
- **Cons:** Require domain knowledge

#### C. Aggregated Features ⭐ **WE CREATE THESE**
```python
# Average over 30 days
mean_return = mean(last_30_days_returns)

# Maximum over all time
max_drawdown = max(all_drawdowns)
```
- **Why:** We need ONE number per stock (not daily data)
- Clustering needs: 1 row = 1 stock, columns = features

---

### 4.4 Feature Scaling (CRITICAL!)

**Problem:**  
Features have different ranges, some dominate clustering!

**Example:**
```
Feature         Stock A    Stock B
Volume          1,000,000  2,000,000  (large numbers)
Return          0.001      0.002      (tiny numbers)
```

**Without Scaling:**
- K-Means uses distance formula: sqrt((x1-x2)² + (y1-y2)²)
- Volume difference = 1,000,000² = HUGE
- Return difference = 0.001² = tiny
- **Result:** Algorithm only considers volume, ignores returns!

**Solution: Scaling**

#### Method 1: StandardScaler (Z-score Normalization)
```python
scaled_value = (value - mean) / std_deviation
```

**Result:** Mean = 0, Std = 1

**Pros:**
- Works well for normal distributions
- Preserves relationships

**Cons:**
- Sensitive to outliers
- One extreme value shifts everything

**Example:**
```
Returns: [1%, 2%, 1.5%, 100%]  ← outlier!
After StandardScaler: all compressed because of 100%
```

---

#### Method 2: RobustScaler ⭐ **WE USE THIS**
```python
scaled_value = (value - median) / IQR
```
- **IQR:** Interquartile Range (75th percentile - 25th percentile)

**Why Better for Finance:**
- Uses median (not mean) → ignores outliers
- Uses IQR (not std) → robust to extremes
- **Example:**
  ```
  Returns: [1%, 2%, 1.5%, 100%]  ← outlier!
  Median = 1.75%, IQR = 0.5%
  Outlier scaled differently, doesn't affect other points
  ```

**Our Code:**
```python
from sklearn.preprocessing import RobustScaler
scaler = RobustScaler()
X_scaled = scaler.fit_transform(X)
```

---

#### Method 3: MinMaxScaler
```python
scaled_value = (value - min) / (max - min)
```
**Result:** All values between 0 and 1

**Pros:** Intuitive range

**Cons:** Very sensitive to outliers (one extreme value changes everything)

**Why We DON'T Use It:** Financial data has extreme events (crashes, booms)

---

**Scaling Decision Summary:**
```
StandardScaler → Use when: data is normal, no outliers
RobustScaler   → Use when: data has outliers (finance!) ✓
MinMaxScaler   → Use when: need specific range (e.g., neural networks)
```

---

## Chapter 5: Technical Indicators Explained

**What are Technical Indicators?**  
Mathematical calculations based on price/volume to predict future movements.

**Two Schools of Thought:**

1. **Fundamental Analysis:** Study company financials, industry, economy
2. **Technical Analysis:** Study charts, patterns, indicators (we use this)

**Our Use:** Indicators help identify stock behavior patterns for clustering

---

### 5.1 Volatility Indicators

#### A. Rolling Volatility ⭐
```python
volatility_7d = returns.rolling(7).std()
```

**What:** Standard deviation of returns over a window

**Why 7, 14, 30 days?**
- 7 days: Short-term jitters (recent news)
- 14 days: Medium-term trends
- 30 days: Long-term stability

**Interpretation:**
- High volatility = unpredictable, risky
- Low volatility = stable, safer
- **Example:**
  - Tech startup: volatility = 5% (wild swings!)
  - Utility company: volatility = 0.5% (boring but steady)

**Real-Life Analogy:**
- Volatility = How bumpy a road is
- High volatility = off-road jeep ride
- Low volatility = smooth highway

---

#### B. Bollinger Bands ⭐
```python
# Middle band = 20-day moving average
middle = price.rolling(20).mean()

# Bands = Middle ± 2 standard deviations
upper = middle + 2 * price.rolling(20).std()
lower = middle - 2 * price.rolling(20).std()

# Width = How far apart bands are
bb_width = (upper - lower) / middle
```

**Visual:**
```
Upper Band  ----------------------  (Price rarely goes above)
                 ~~~~~~
Price --------  ~~~~~~~~  --------  (Bounces between bands)
                 ~~~~~~
Lower Band  ----------------------  (Price rarely goes below)
```

**Interpretation:**

**1. Band Width:**
- **Wide bands:** High volatility (price swinging a lot)
- **Narrow bands:** Low volatility (price stable)

**2. Price Position:**
- **Near upper band:** Potentially overbought (might drop soon)
- **Near lower band:** Potentially oversold (might rise soon)
- **At middle:** Neutral

**Our Use:**
```python
bb_width_mean = mean(bb_width over all days)
bb_position_mean = mean((price - lower) / (upper - lower))
```
- `bb_width_mean`: Average volatility measure
- `bb_position_mean`: Does stock trend high or low in its range?

---

### 5.2 Momentum Indicators

**Momentum:** Rate of price change (speed of movement)

**Analogy:**  
- Car going 0 → 60 mph quickly = high momentum
- Stock price rising fast = high momentum (bullish!)

---

#### A. Simple Momentum ⭐
```python
momentum_30d = (price_today - price_30_days_ago) / price_30_days_ago
```

**Interpretation:**
- **Positive:** Price rising (uptrend)
- **Negative:** Price falling (downtrend)
- **Example:**
  - momentum_30d = +0.15 (15% gain in 30 days) → Strong uptrend!
  - momentum_30d = -0.10 (10% loss) → Downtrend

**Our Use:**
```python
momentum_30d = last_momentum_value  # Latest trend
momentum_90d = 90_day_momentum      # Longer-term trend
```

---

#### B. Moving Averages (MA)
```python
ma_7 = price.rolling(7).mean()    # Short-term
ma_30 = price.rolling(30).mean()   # Medium-term
ma_50 = price.rolling(50).mean()   # Long-term
```

**What:** Average price over N days (smooths noise)

**Visual:**
```
Price (noisy): \/\/\/\/\/\/\  ← Hard to see trend
MA (smooth):   ___/‾‾‾‾‾\_    ← Clear uptrend then downtrend
```

**Trading Signals:**

**1. Golden Cross (Bullish):**
```
Short-term MA crosses ABOVE long-term MA
→ Price gaining momentum, buy signal!
```

**2. Death Cross (Bearish):**
```
Short-term MA crosses BELOW long-term MA
→ Price losing momentum, sell signal!
```

**Our Use:**
```python
price_to_ma30 = current_price / ma_30
price_to_ma50 = current_price / ma_50
```
- **> 1:** Price above average (strong)
- **< 1:** Price below average (weak)
- **Example:** price_to_ma30 = 1.10 means stock is 10% above its 30-day average

---

#### C. RSI (Relative Strength Index) ⭐
```python
# Step 1: Separate gains and losses
gains = [max(0, return) for return in returns]
losses = [abs(min(0, return)) for return in returns]

# Step 2: Average over 14 days
avg_gain = mean(gains[-14:])
avg_loss = mean(losses[-14:])

# Step 3: Relative Strength
RS = avg_gain / avg_loss

# Step 4: RSI formula
RSI = 100 - (100 / (1 + RS))
```

**Range:** 0 to 100

**Interpretation:**
```
RSI > 70  → Overbought (might drop soon) 🔴
RSI 30-70 → Neutral (healthy range) ✅
RSI < 30  → Oversold (might rise soon) 🟢
```

**Example:**
- Stock has RSI = 85 for a week → Probably due for a correction (drop)
- Stock has RSI = 20 → Might be a buying opportunity

**Our Use:**
```python
rsi_mean = mean(RSI over all days)
```
- High rsi_mean (>60): Stock tends to be overbought (high momentum, risky)
- Low rsi_mean (<40): Stock tends to be oversold (low momentum, stable)

**Real-Life Analogy:**
- RSI = How "tired" a runner is
- RSI > 70 = Sprinting too long, needs to rest (price will drop)
- RSI < 30 = Rested, ready to run (price will rise)

---

#### D. MACD (Moving Average Convergence Divergence)
```python
# Step 1: Calculate two EMAs (Exponential Moving Averages)
ema_12 = price.ewm(span=12).mean()  # Fast-moving
ema_26 = price.ewm(span=26).mean()  # Slow-moving

# Step 2: MACD Line
macd_line = ema_12 - ema_26

# Step 3: Signal Line (smooth MACD)
signal_line = macd_line.ewm(span=9).mean()

# Step 4: Histogram (difference)
macd_histogram = macd_line - signal_line
```

**What It Shows:**

**1. MACD Line:**
- **Positive:** Short-term trend stronger than long-term (bullish)
- **Negative:** Short-term weaker (bearish)

**2. Signal Line:**
- Smoothed version of MACD (filters noise)

**3. Crossovers:**
- **MACD crosses above Signal:** Buy signal (momentum increasing)
- **MACD crosses below Signal:** Sell signal (momentum decreasing)

**Our Use:**
```python
macd_volatility = std(macd_line)
```
- High MACD volatility = momentum changes frequently (unpredictable, risky)
- Low MACD volatility = steady momentum (predictable, safer)

---

### 5.3 Risk Metrics

#### A. Standard Deviation (Simple Volatility)
```python
std_return = np.std(returns)
```
- **What:** How spread out returns are
- **High std:** Returns all over the place (risky)
- **Low std:** Returns clustered near average (safe)

**Example:**
```
Stock A returns: [1%, 2%, 1%, 2%] → std = 0.5% (low risk)
Stock B returns: [-10%, 15%, -5%, 20%] → std = 14% (high risk!)
```

---

#### B. Downside Deviation ⭐ (Better Than Std)
```python
# Only consider NEGATIVE returns
negative_returns = [r for r in returns if r < 0]
downside_deviation = np.sqrt(np.mean([r**2 for r in negative_returns]))
```

**Why Better:**
- Standard deviation penalizes BOTH upside and downside volatility
- Investors don't mind upside volatility (big gains are good!)
- **Downside deviation only measures bad volatility (losses)**

**Example:**
```
Stock A: Returns = [+20%, +25%, +18%] → std high, but all gains!
Stock B: Returns = [+5%, -15%, +10%] → std similar, but has losses

Downside Deviation:
Stock A: 0% (no losses!)
Stock B: 15% (big loss!)
```

**Our Use:**
```python
downside_deviation = sqrt(mean([r**2 for r in returns if r < 0]))
```
- High downside deviation = expect painful losses
- Low downside deviation = losses are mild

---

#### C. Value at Risk (VaR) ⭐
```python
var_95 = np.percentile(returns, 5)
```

**What:** "In the worst 5% of days, how much do I lose?"

**Interpretation:**
- VaR_95 = -5% means:
  - 95% of days: Loss is less than 5%
  - 5% of days (worst days): Loss exceeds 5%

**Example:**
```
Stock A: VaR_95 = -2% (worst days lose 2%)
Stock B: VaR_95 = -10% (worst days lose 10%) ← Much riskier!
```

**Real-Life Analogy:**
- VaR = "How bad can it get?"
- Like checking flood risk: "In worst storms, water rises 5 feet"

**Our Use:**
```python
var_95 = np.percentile(returns, 5)  # 5th percentile
```
- Captures tail risk (extreme events)
- Important for conservative investors

---

#### D. Maximum Drawdown ⭐
```python
# Calculate cumulative maximum (peak)
cummax = price.expanding().max()

# Drawdown = how far below peak
drawdown = (price - cummax) / cummax

# Maximum drawdown = worst drop
max_drawdown = drawdown.min()
```

**What:** Largest peak-to-trough decline

**Example:**
```
Jan: $100 (peak)
Feb: $90
Mar: $70 (trough) → Drawdown = -30%
Apr: $80
May: $95

Max Drawdown = -30%
```

**Why Scary:**
- Shows worst-case scenario
- 50% drawdown means you need 100% gain to break even!
  - $100 → $50 (-50%)
  - $50 → $100 (+100% needed!)

**Our Use:**
```python
max_drawdown = min(drawdown over all time)
```
- High max_drawdown (e.g., -60%) = very risky stock
- Low max_drawdown (e.g., -10%) = stable stock

---

#### E. Sharpe Ratio ⭐⭐⭐ (MOST IMPORTANT!)
```python
sharpe_ratio = (mean_return - risk_free_rate) / std_return
```

**What:** Return per unit of risk (risk-adjusted performance)

**Components:**

**1. Excess Return:**
```python
excess_return = mean_return - risk_free_rate
```
- How much MORE than "safe" investment (e.g., government bonds)
- Risk-free rate ≈ 0.01% daily (≈4% annually for treasury bills)

**2. Risk (Volatility):**
```python
risk = std_return
```

**3. Ratio:**
```python
sharpe = excess_return / risk
```

**Interpretation:**
```
Sharpe > 2   → Excellent (high return for the risk)
Sharpe 1-2   → Good
Sharpe 0.5-1 → Moderate
Sharpe < 0.5 → Poor (not worth the risk)
Sharpe < 0   → Losing money (worse than risk-free!)
```

**Example:**

**Stock A:**
- Mean return: 2% per month
- Std dev: 5%
- Sharpe = (2% - 0%) / 5% = 0.4

**Stock B:**
- Mean return: 1.5% per month
- Std dev: 1%
- Sharpe = (1.5% - 0%) / 1% = 1.5

**Result:** Stock B is BETTER! Lower return but MUCH lower risk (higher Sharpe).

**Why We Cap at -5 to +5:**
```python
sharpe_ratio = np.clip(sharpe, -5, 5)
```
- Extreme values (e.g., ±100) occur when:
  - Very low volatility (dividing by tiny number)
  - Data errors
- Extreme values dominate clustering (algorithm focuses only on them)
- Capping preserves relative ranking without distortion

**Real-Life Analogy:**
- Sharpe Ratio = Miles per gallon (MPG) for cars
- High MPG = efficient (good return for fuel used)
- High Sharpe = efficient (good return for risk taken)

---

### 5.4 Liquidity Metrics

**Liquidity:** How easily you can buy/sell without affecting price

**Example:**
- **Liquid (High Volume):** Safaricom - millions of shares traded daily
  - You can sell 1000 shares instantly at market price
- **Illiquid (Low Volume):** Small company - 100 shares traded daily
  - You try to sell 1000 shares → No buyers! Must lower price drastically

---

#### A. Trading Frequency
```python
trading_frequency = trading_days / total_days
```

**What:** How often stock trades (active trading days / calendar days)

**Example:**
```
252 trading days in a year
Stock A traded 250 days → frequency = 99% (very liquid)
Stock B traded 50 days → frequency = 20% (illiquid!)
```

**Why Important:**
- Low frequency = might not be able to sell when you want
- High frequency = always buyers/sellers available

---

#### B. Average Volume
```python
avg_volume = mean(daily_volume over 30 days)
```

**Interpretation:**
- High volume = popular stock, easy to trade
- Low volume = hard to exit position

**Example:**
- Safaricom: 10M shares/day (you can trade anytime)
- Small stock: 1K shares/day (you might move the market!)

---

#### C. Volume Volatility
```python
volume_volatility = std(daily_volume) / mean(daily_volume)
```

**What:** How consistent trading volume is

**High Volume Volatility:**
- Some days 1K shares, other days 100K shares
- Unpredictable liquidity (risky!)
- Often due to news events

**Low Volume Volatility:**
- Consistently 50K shares daily
- Predictable liquidity (safe)

---

#### D. Amihud Illiquidity Ratio ⭐
```python
amihud = abs(daily_return) / daily_volume_dollars
```

**What:** Price impact per dollar traded

**Interpretation:**
- **High Amihud:** Small trades move price a lot (illiquid!)
- **Low Amihud:** Big trades barely affect price (liquid)

**Example:**

**Stock A (Liquid):**
- $1M traded → price moves 0.1%
- Amihud = 0.001 / 1,000,000 = 0.000000001

**Stock B (Illiquid):**
- $10K traded → price moves 5%
- Amihud = 0.05 / 10,000 = 0.000005 (much higher!)

**Our Use:**
```python
amihud_illiquidity = median(daily_amihud)
```
- High value = illiquid stock (risky!)
- Low value = liquid stock (safe)

---

## Chapter 6: Risk Metrics in Portfolio Management

### 6.1 Return Distributions (Skewness & Kurtosis)

#### A. Skewness ⭐
```python
return_skew = scipy.stats.skew(returns)
```

**What:** Asymmetry of return distribution

**Visual:**
```
NEGATIVE SKEW (< 0):          POSITIVE SKEW (> 0):
    |                              |
   /|                              |\
  / |                              | \
 /  |__                          __  \
```

**Interpretation:**

**Negative Skew (Bad!):**
- Many small gains, few HUGE losses
- Example: Returns = [+1%, +2%, +1%, -20%]
- **Why Bad:** Slow gains, sudden crashes (worst for investors!)
- **Example Stocks:** High-leverage companies (can crash quickly)

**Positive Skew (Good!):**
- Many small losses, few HUGE gains
- Example: Returns = [-1%, -0.5%, +0%, +25%]
- **Why Good:** Occasional jackpots, limited downside
- **Example Stocks:** Lottery-like stocks (biotech, tech startups)

**Zero Skew:**
- Symmetric distribution (rare in real stocks)
- Normal bell curve

**Our Use:**
```python
return_skew = skew(returns)
```
- Negative skew = higher risk (crash potential)
- Positive skew = lower risk (upside potential)

---

#### B. Kurtosis ⭐
```python
return_kurtosis = scipy.stats.kurtosis(returns)
```

**What:** "Tailedness" - how often extreme events occur

**Visual:**
```
LOW KURTOSIS:           HIGH KURTOSIS:
    |                       |
   / \                     /|\
  /   \                   / | \
 /     \               __/  |  \__
         ← Thin tails      ← Fat tails
```

**Interpretation:**

**High Kurtosis (Fat Tails) - RISKY:**
- Extreme events (crashes/booms) more common than expected
- Example: Returns = [0%, 0%, 0%, -30%, +40%] ← Extreme swings!
- **Why Risky:** "Black swan" events happen often
- **Example:** Cryptocurrency, penny stocks

**Low Kurtosis (Thin Tails) - SAFE:**
- Extreme events rare
- Returns mostly near average
- Example: Returns = [1%, 2%, 1.5%, 2%]
- **Example:** Utility companies, consumer staples

**Our Use:**
```python
return_kurtosis = kurtosis(returns)
```
- High kurtosis = expect surprises (good or bad) → Higher risk
- Low kurtosis = predictable behavior → Lower risk

**Why Skew & Kurtosis Matter:**
- Standard deviation assumes normal distribution (bell curve)
- Real stock returns are NOT normal!
- Skew and kurtosis capture this non-normality
- **Example:**
  - Stock A: std = 5%, skew = -2, kurtosis = 10 (risky!)
  - Stock B: std = 5%, skew = 0, kurtosis = 0 (safer)
  - Same volatility, but A much riskier due to crash potential

---

### 6.2 Risk-Adjusted Performance (Putting It All Together)

**The Big Question:**  
"Is this stock's return worth its risk?"

**Bad Metric (Return Only):**
```
Stock A: +30% return (sounds great!)
... but 60% volatility (wild swings!)
```

**Good Metrics (Risk-Adjusted):**

#### 1. Sharpe Ratio (We covered this)
```python
sharpe = mean_return / std_return
```
- Higher = better return per risk
- **Use Case:** Compare any two investments
- **Limitation:** Treats upside and downside volatility equally

---

#### 2. Sortino Ratio (Better Than Sharpe!)
```python
sortino = mean_return / downside_deviation
```
- **Advantage:** Only penalizes downside volatility
- Higher = better return per downside risk
- **More realistic:** Investors don't mind gains, only losses!
- **Why We Don't Use It:** Sharpe is industry standard (easier to explain)

---

#### 3. Information Ratio
```python
information_ratio = (portfolio_return - benchmark_return) / tracking_error
```
- **What:** Return vs. benchmark (e.g., S&P 500) per tracking risk
- **Use Case:** Evaluate fund managers
- **Not Used Here:** We don't have benchmark data

---

### 6.3 Portfolio Construction (Why Our Clustering Helps)

**Modern Portfolio Theory (Harry Markowitz, Nobel Prize):**

**Key Idea:**  
Don't put all eggs in one basket! Diversify to reduce risk.

**Efficient Frontier:**
```
Return
   |     * (Portfolio B)
   |    *
   |   * ← Efficient Frontier (best risk-return)
   |  *
   | *
   |* (Portfolio A)
   +------------------→ Risk
```

**How to Build Efficient Portfolio:**
1. Choose desired risk level (e.g., "I can handle 10% volatility")
2. Pick stocks from multiple risk clusters
3. Weight them to achieve target risk
4. Maximize return for that risk

**Our Project Helps:**
```
Conservative Investor (30% portfolio risk):
- 70% Low Risk stocks
- 20% Medium-Low
- 10% Medium-High
- 0% High Risk

Aggressive Investor (60% portfolio risk):
- 10% Low Risk (stability)
- 20% Medium-Low
- 30% Medium-High
- 40% High Risk (growth potential)
```

**Without Our Clustering:**
- Investor must analyze 57 stocks individually (hours of work!)

**With Our Clustering:**
- Investor sees 4 groups, picks ratio → Done in minutes!

---

This is the end of PART 1. Let me know when you're ready for PART 2, which will cover:
- Line-by-line code explanation of `features.py`
- Line-by-line code explanation of `clustering.py`
- Notebooks deep-dive

Would you like me to continue with PART 2 now?

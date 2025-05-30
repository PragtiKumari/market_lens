# scripts/price_sensitivity.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# 🔹 Load Data
df = pd.read_csv("data/processed/ads_cleaned.csv")
print("📦 Data Loaded:")
print(df.head())

# 🔸 Simulate Price and Revenue for Analysis
np.random.seed(42)
df['price'] = np.random.uniform(10, 100, size=len(df))
df['click'] = df['click'].fillna(0)  # Ensure clicks are numeric
df['revenue'] = df['click'] * df['price']

print("\n💰 Sample Revenue Data:")
print(df[['id', 'price', 'click', 'revenue']].head())

# 🔹 Visualize Price vs Click Rate
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x='price', y='click', alpha=0.6)
plt.title("💸 Price vs Clicks")
plt.xlabel("Ad Price")
plt.ylabel("Clicks")
plt.grid(True)
plt.tight_layout()
plt.show()

# 🔸 Train Linear Regression Model to Check Sensitivity
X = df[['price']]
y = df['click']

model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)

# 🔹 Display Model Metrics
print("\n📉 Price Sensitivity Model:")
print(f"Slope (Price Coefficient): {model.coef_[0]:.4f}")
print(f"Intercept: {model.intercept_:.4f}")
print(f"R-squared: {r2_score(y, y_pred):.4f}")

# 🔸 Visualize Regression Line
plt.figure(figsize=(8, 5))
sns.scatterplot(x=df['price'], y=df['click'], alpha=0.5, label="Actual")
plt.plot(df['price'], y_pred, color='red', label="Regression Line")
plt.title("🧠 Price Sensitivity (Regression)")
plt.xlabel("Price")
plt.ylabel("Clicks")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ✅ Save final data with price & revenue to CSV
df.to_csv("data/processed/price_sensitivity.csv", index=False)
print("✅ price_sensitivity.csv saved in data/processed/")

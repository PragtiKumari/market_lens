import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load data
df = pd.read_csv('data/processed/ads_cleaned.csv')
print("📦 Data Loaded:\n", df.head())

# Simulate purchase value and frequency (demo purpose)
np.random.seed(42)
df['purchase_value'] = np.random.uniform(20, 200, size=len(df))
df['purchase_frequency'] = np.random.randint(1, 10, size=len(df))

# Calculate CLV
df['CLV'] = df['purchase_value'] * df['purchase_frequency']

print("\n💰 Sample CLV Data:\n", df[['id', 'purchase_value', 'purchase_frequency', 'CLV']].head())

# Scale CLV for clustering
scaler = StandardScaler()
df['CLV_scaled'] = scaler.fit_transform(df[['CLV']])

# Cluster customers based on CLV
kmeans = KMeans(n_clusters=3, random_state=42)
df['CLV_segment'] = kmeans.fit_predict(df[['CLV_scaled']])

# Rename segments
segment_map = {
    0: 'Low CLV',
    1: 'Medium CLV',
    2: 'High CLV'
}
df['CLV_segment'] = df['CLV_segment'].map(lambda x: segment_map.get(x, 'Unknown'))

# 📊 Visualize
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x='CLV_segment', y='CLV', palette='Set2')
plt.title("💎 Customer Segments based on CLV")
plt.xlabel("CLV Segment")
plt.ylabel("Customer Lifetime Value")
plt.tight_layout()
plt.show()

# ✅ Save the CLV data to CSV
df.to_csv("data/processed/clv.csv", index=False)
print("✅ clv.csv saved in data/processed/")

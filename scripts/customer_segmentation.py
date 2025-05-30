import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings("ignore")


df = pd.read_csv("data/processed/retail_cleaned.csv")
print(df.head())


# Force convert InvoiceDate to datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')

# Drop rows where InvoiceDate conversion failed (just in case)
df = df.dropna(subset=['InvoiceDate', 'CustomerID'])

# Create TotalAmount column if not already present
if 'TotalAmount' not in df.columns:
    df['TotalAmount'] = df['Quantity'] * df['UnitPrice']


snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'InvoiceNo': 'nunique',
    'TotalAmount': 'sum'
})

rfm.rename(columns={
    'InvoiceDate': 'Recency',
    'InvoiceNo': 'Frequency',
    'TotalAmount': 'Monetary'
}, inplace=True)

print(rfm.head())


scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm)

kmeans = KMeans(n_clusters=4, random_state=42)
rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)

print(rfm.head())


sns.scatterplot(data=rfm, x='Recency', y='Monetary', hue='Cluster', palette='Set2')
plt.title('Customer Segments')
plt.show()


rfm.to_csv("data/processed/customer_segments.csv")
print("Segmented data saved successfully! 🥳")


import matplotlib.pyplot as plt
import seaborn as sns

# Set plot style
sns.set(style="whitegrid")

# Rename clusters for better understanding
cluster_map = {
    0: 'High Value',
    1: 'Low Value',
    2: 'Mid Value',
    3: 'Budget Shopper'  # You have 4 clusters, so let's label 4
}
rfm['Segment'] = rfm['Cluster'].map(cluster_map)

# Plot Recency vs Monetary by Segment
plt.figure(figsize=(10,6))
sns.scatterplot(data=rfm, x='Recency', y='Monetary', hue='Segment', palette='viridis', s=100)
plt.title('Customer Segments: Recency vs Monetary')
plt.savefig('outputs/recency_vs_monetary.png')
plt.show()

# Summary statistics by cluster
segment_summary = rfm.groupby('Segment').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': 'mean'
}).round(2)

print("\nSegment Summary:")
print(segment_summary)

# Save each segment into a separate CSV
for segment in rfm['Segment'].unique():
    segment_df = rfm[rfm['Segment'] == segment]
    filename = f"outputs/{segment.replace(' ', '_').lower()}_customers.csv"
    segment_df.to_csv(filename)

print("All segment files saved separately 🗂️")


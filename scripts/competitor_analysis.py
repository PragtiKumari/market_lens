import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
data_path = "data/processed/mock_kaggle_cleaned.csv"
df = pd.read_csv(data_path)

# Rename columns for simplicity
df = df.rename(columns={
    'data': 'Date',
    'venda': 'Sales',
    'estoque': 'Stock',
    'preco': 'Price'
})

# Convert date column
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# ✅ Step 1: Total sales over time
df.set_index('Date')['Sales'].plot(title='Total Sales Over Time', figsize=(10,5), color='green')
plt.ylabel('Sales')
plt.grid(True)
plt.tight_layout()
plt.show()

# ✅ Step 2: Price vs Sales scatter
plt.figure(figsize=(10,6))
sns.scatterplot(data=df, x='Price', y='Sales')
plt.title('Price vs Sales')
plt.xlabel('Product Price')
plt.ylabel('Units Sold')
plt.grid(True)
plt.tight_layout()
plt.show()

# ✅ Step 3: Save cleaned + renamed + sorted data as competitor_data.csv
df.to_csv("data/processed/competitor_data.csv", index=False)
print("✅ competitor_data.csv saved in data/processed/")


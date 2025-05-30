import pandas as pd
import numpy as np

# Load the cleaned data
df = pd.read_csv('data/processed/ads_cleaned.csv')

# 🧠 Add dummy 'segment' values based on age
try:
    df['segment'] = pd.qcut(df['age'], q=4, labels=['Young', 'Mid-Young', 'Mid-Old', 'Old'])
except:
    df['segment'] = 'Unknown'  # fallback if age missing

# 💸 Add dummy CLV values
df['clv'] = np.random.randint(500, 10000, size=len(df))

# Save it again
df.to_csv('data/final_output.csv', index=False)
print("✅ final_output.csv is ready with 'segment' and 'clv' columns.")

import pandas as pd

df = pd.read_csv('data/final_output.csv')
print("\n📄 Columns in final_output.csv:")
print(df.columns)
print("\n👀 First few rows:")
print(df.head())

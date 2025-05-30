import pandas as pd

# Load datasets safely
retail = pd.read_csv("data/raw/Online Retail.csv", encoding='ISO-8859-1', on_bad_lines='skip')
sell_1 = pd.read_csv("data/raw/SELL_1.csv", sep=';', encoding='ISO-8859-1', on_bad_lines='skip')
ads = pd.read_csv("data/raw/ad_click_dataset.csv", encoding='ISO-8859-1', on_bad_lines='skip')
day_sell = pd.read_csv("data/raw/Day_sell_24_12_18.csv", encoding='ISO-8859-1', on_bad_lines='skip')
rotation = pd.read_csv("data/raw/ROTATION_of_products01.01.2018-09.01.2019.csv", encoding='ISO-8859-1', on_bad_lines='skip')
mock = pd.read_csv("data/raw/mock_kaggle.csv", encoding='ISO-8859-1', on_bad_lines='skip')

# Preview each one
print("Retail:\n", retail.head(), "\n")
print("SELL_1:\n", sell_1.head(), "\n")
print("Ads:\n", ads.head(), "\n")
print("Day Sell:\n", day_sell.head(), "\n")
print("Rotation:\n", rotation.head(), "\n")
print("Mock Kaggle:\n", mock.head(), "\n")

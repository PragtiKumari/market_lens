import pandas as pd
import os

# Paths
RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed"

# Helper function to save cleaned data
def save_cleaned(df, name):
    output_path = os.path.join(PROCESSED_PATH, f"{name}_cleaned.csv")
    df.to_csv(output_path, index=False)
    print(f"\u2705 Saved cleaned data: {output_path}")

# 1. Retail Dataset
def clean_retail():
    print("\nCleaning Retail dataset...")
    path = os.path.join(RAW_PATH, "Retail.csv")
    if not os.path.exists(path):
        print(f"\u274C File not found: {path}")
        return

    df = pd.read_csv(path, encoding='ISO-8859-1')

    df.dropna(subset=["InvoiceNo", "Description", "CustomerID"], inplace=True)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors='coerce')
    df = df[df["Quantity"] > 0]
    df = df[df["UnitPrice"] > 0]

    save_cleaned(df, "retail")

# 2. Sell_1 Dataset
def clean_sell1():
    print("\nCleaning Sell_1 dataset...")
    path = os.path.join(RAW_PATH, "SELL_1.csv")
    if not os.path.exists(path):
        print(f"\u274C File not found: {path}")
        return

    df = pd.read_csv(path, delimiter=";", encoding='ISO-8859-1')
    df.columns = df.columns.str.strip()
    df.dropna(subset=["Pgroup", "Pname", "pce_zn"], inplace=True)
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors='coerce')

    numeric_cols = ["pce_zn", "pwa_sb", "pudzsb", "pmarza", "pmarzajedn", "pkwmarza", "pudzmarza"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(",", ".")
            df[col] = pd.to_numeric(df[col], errors="coerce")

    save_cleaned(df, "sell_1")

# 3. Ads Dataset
def clean_ads():
    print("\nCleaning Ads dataset...")
    path = os.path.join(RAW_PATH, "Ads.csv")
    if not os.path.exists(path):
        print(f"\u274C File not found: {path}")
        return

    df = pd.read_csv(path)

    df.dropna(subset=["age", "gender", "device_type"], inplace=True)
    df["time_of_day"] = df["time_of_day"].fillna("Unknown")

    save_cleaned(df, "ads")

# 4. Day Sell Dataset
def clean_day_sell():
    print("\nCleaning Day Sell dataset...")
    path = os.path.join(RAW_PATH, "Day Sell.csv")
    if not os.path.exists(path):
        print(f"\u274C File not found: {path}")
        return

    df = pd.read_csv(path, sep=";")
    df.columns = ["Date", "zn", "sb", "tax", "marza"]
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors='coerce')

    for col in ["zn", "sb", "tax", "marza"]:
        df[col] = df[col].astype(str).str.replace(" ", "").str.replace(",", ".")
        df[col] = pd.to_numeric(df[col], errors="coerce")

    save_cleaned(df, "day_sell")

# 5. Rotation Dataset
def clean_rotation():
    path = os.path.join(RAW_PATH, "Rotation.csv")
    df = pd.read_csv(path, sep=";", encoding="ISO-8859-1")

    df.columns = df.columns.str.strip()
    df.dropna(how="all", inplace=True)

    save_cleaned(df, "rotation")

# 6. Mock Kaggle Dataset
def clean_mock_kaggle():
    print("\nCleaning Mock Kaggle dataset...")
    path = os.path.join(RAW_PATH, "Mock Kaggle.csv")
    if not os.path.exists(path):
        print(f"\u274C File not found: {path}")
        return

    df = pd.read_csv(path)
    if "data" not in df.columns:
        if "date" in df.columns:
            df.rename(columns={"date": "data"}, inplace=True)

    df["data"] = pd.to_datetime(df["data"], errors='coerce')
    df = df.dropna()
    df = df[df["preco"] > 0]

    save_cleaned(df, "mock_kaggle")

# Run all cleaning functions
if __name__ == "__main__":
    clean_retail()
    clean_sell1()
    clean_ads()
    clean_day_sell()
    clean_rotation()
    clean_mock_kaggle()
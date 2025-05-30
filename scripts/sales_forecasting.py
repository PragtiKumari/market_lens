import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Load the data
data_path = 'data/processed/day_sell_cleaned.csv'
df = pd.read_csv(data_path, parse_dates=['Date'])

# Set Date as index
df.set_index('Date', inplace=True)

# Resample daily (fill missing dates)
df = df.resample('D').mean().interpolate()

# Drop rows with any remaining NaNs
df.dropna(inplace=True)

# Forecast each metric one by one
metrics = ['zn', 'sb', 'tax', 'marza']
forecast_days = 30

# --- NEW: Create a dictionary to collect all forecasts ---
all_forecasts = {}

for metric in metrics:
    print(f"\n📊 Forecasting for: {metric}")

    # Build and fit the model
    model = ExponentialSmoothing(df[metric], trend='add', seasonal='add', seasonal_periods=7)
    fit = model.fit()

    # Forecast future values
    forecast = fit.forecast(forecast_days)

    # Save forecast values to dictionary
    all_forecasts[metric] = forecast.values

    # Plot
    plt.figure(figsize=(12, 5))
    plt.plot(df[metric], label=f'Actual {metric}')
    plt.plot(forecast, label=f'Forecasted {metric}', color='red')
    plt.title(f'30-Day Forecast for {metric.upper()}')
    plt.xlabel('Date')
    plt.ylabel(metric.upper())
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# --- NEW: Create a DataFrame from the forecasts ---
result = pd.DataFrame(all_forecasts)

# Add a date column for the next 30 days
result['Date'] = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=forecast_days)

# Reorder to keep Date in front
result = result[['Date'] + metrics]

# Save the forecast result to CSV
result.to_csv("data/processed/sales_forecast.csv", index=False)
print("✅ sales_forecast.csv saved in data/processed/")

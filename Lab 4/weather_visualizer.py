import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# Task 1: Load the Dataset
# ---------------------------

df = pd.read_csv("daily_weather_data.csv")

print("First 5 rows:")
print(df.head())

print("\nDataset Info:")
print(df.info())

print("\nStatistical Summary:")
print(df.describe())

# ---------------------------
# Task 2: Data Cleaning
# ---------------------------

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Fill missing values
df['temperature'] = df['temperature'].fillna(df['temperature'].mean())
df['humidity'] = df['humidity'].fillna(df['humidity'].mean())
df['rainfall'] = df['rainfall'].fillna(0)

# Select necessary columns
df = df[['date', 'temperature', 'humidity', 'rainfall']]

# ---------------------------
# Task 3: Statistical Analysis
# ---------------------------

daily_mean_temp = np.mean(df['temperature'])
max_temp = np.max(df['temperature'])
min_temp = np.min(df['temperature'])

print("\nDaily Mean Temperature:", daily_mean_temp)
print("Max Temperature:", max_temp)
print("Min Temperature:", min_temp)

# Add month and year
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

# ---------------------------
# Task 4: Visualizations
# ---------------------------

# Line Plot – Daily Temperature
plt.figure(figsize=(10, 5))
plt.plot(df['date'], df['temperature'])
plt.title("Daily Temperature Trend")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.savefig("daily_temperature.png")
plt.show()

# Bar Chart – Monthly Rainfall
monthly_rainfall = df.groupby('month')['rainfall'].sum()

plt.figure(figsize=(10, 5))
monthly_rainfall.plot(kind='bar')
plt.title("Monthly Rainfall Totals")
plt.xlabel("Month")
plt.ylabel("Rainfall (mm)")
plt.savefig("monthly_rainfall.png")
plt.show()

# Scatter Plot – Humidity vs Temperature
plt.figure(figsize=(8, 5))
plt.scatter(df['humidity'], df['temperature'])
plt.title("Humidity vs Temperature")
plt.xlabel("Humidity (%)")
plt.ylabel("Temperature (°C)")
plt.savefig("humidity_vs_temperature.png")
plt.show()

# Combined Plot
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(df['date'], df['temperature'], color='blue')
plt.title("Temperature Trend")

plt.subplot(1, 2, 2)
plt.scatter(df['humidity'], df['temperature'], color='green')
plt.title("Humidity vs Temp")

plt.savefig("combined_plot.png")
plt.show()

# ---------------------------
# Task 5: Grouping
# ---------------------------

month_group = df.groupby('month').agg({
    'temperature': 'mean',
    'rainfall': 'sum',
    'humidity': 'mean'
})

print("\nMonthly Summary:")
print(month_group)

# ---------------------------
# Task 6: Exporting Outputs
# ---------------------------

df.to_csv("cleaned_weather.csv", index=False)
month_group.to_csv("monthly_summary.csv")

print("\nAll tasks completed successfully!")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
from datetime import datetime



class MeterReading:
    def _init_(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh


class Building:
    def _init_(self, name):
        self.name = name
        self.meter_readings = []

    def add_reading(self, reading):
        self.meter_readings.append(reading)

    def calculate_total_consumption(self):
        return sum(r.kwh for r in self.meter_readings)

    def generate_report(self):
        total = self.calculate_total_consumption()
        return f"Building: {self.name}, Total kWh: {total}"


class BuildingManager:
    def _init_(self):
        self.buildings = {}

    def add_building(self, name):
        if name not in self.buildings:
            self.buildings[name] = Building(name)

    def add_reading(self, building_name, timestamp, kwh):
        reading = MeterReading(timestamp, kwh)
        self.buildings[building_name].add_reading(reading)

    def generate_all_reports(self):
        return [b.generate_report() for b in self.buildings.values()]




def load_energy_data():
    data_folder = Path("data")
    csv_files = list(data_folder.glob("*.csv"))

    all_data = []

    for file in csv_files:
        try:
            df = pd.read_csv(file)
            df['building'] = file.stem
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            df = df.dropna(subset=['timestamp', 'kwh'])

            all_data.append(df)

        except Exception as e:
            print(f"Error loading {file.name}: {e}")

    if not all_data:
        raise ValueError("No valid CSV files found.")

    return pd.concat(all_data, ignore_index=True)




def calculate_daily_totals(df):
    return df.resample('D', on='timestamp')['kwh'].sum()


def calculate_weekly_aggregates(df):
    return df.resample('W', on='timestamp')['kwh'].sum()


def building_wise_summary(df):
    return df.groupby('building')['kwh'].agg(['mean', 'max', 'min', 'sum'])



def create_dashboard(daily, weekly, summary, df):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

   
    axes[0].plot(daily.index, daily.values)
    axes[0].set_title("Daily Campus Consumption")
    axes[0].set_xlabel("Date")
    axes[0].set_ylabel("kWh")

   
    axes[1].bar(weekly.index.astype(str), weekly.values)
    axes[1].set_title("Weekly Total Usage")
    axes[1].set_xticklabels(weekly.index.strftime("%Y-%m-%d"), rotation=45)

   
    axes[2].scatter(df['timestamp'], df['kwh'])
    axes[2].set_title("Peak Hour Consumption")
    axes[2].set_xlabel("Time")
    axes[2].set_ylabel("kWh")

    plt.tight_layout()
    Path("output").mkdir(exist_ok=True)
    plt.savefig("output/dashboard.png")
    plt.close()



def generate_summary(df, summary_table):
    total = df['kwh'].sum()
    top_building = summary_table['sum'].idxmax()
    peak_time = df.loc[df['kwh'].idxmax(), 'timestamp']

    summary_text = f"""
    CAMPUS ENERGY SUMMARY
    ----------------------
    Total Campus Consumption: {total} kWh
    Highest Consuming Building: {top_building}
    Highest Peak Time Load: {peak_time}

    Monthly / Weekly trends saved in output folder.
    """

    with open("output/summary.txt", "w") as f:
        f.write(summary_text)

    print(summary_text)




def main():
    print("Loading data...")
    df = load_energy_data()

    # Export cleaned data
    Path("output").mkdir(exist_ok=True)
    df.to_csv("output/cleaned_energy_data.csv", index=False)

    print("Calculating aggregations...")
    daily = calculate_daily_totals(df)
    weekly = calculate_weekly_aggregates(df)
    summary_table = building_wise_summary(df)

    summary_table.to_csv("output/building_summary.csv")

    print("Generating dashboard...")
    create_dashboard(daily, weekly, summary_table, df)

    print("Creating summary report...")
    generate_summary(df, summary_table)

    print("All tasks completed successfully!")

if __name__ == "_main_":
    main()
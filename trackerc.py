# tracker.py
# Author: Your Name
# Date: 19th Sept, 2024
# Project: Daily Calorie Tracker CLI

import datetime

print("======================================")
print("   Welcome to the Daily Calorie Tracker")
print("======================================")
print("This tool helps you log your meals, track calories,")
print("and compare against your daily calorie limit.\n")



meals = []
calories = []

num_meals = int(input("How many meals would you like to enter today? "))

for i in range(num_meals):
    meal_name = input(f"\nEnter meal {i+1} name: ")
    cal = float(input(f"Enter calories for {meal_name}: "))
    
    meals.append(meal_name)
    calories.append(cal)



total_cal = sum(calories)
avg_cal = total_cal / len(calories)

daily_limit = float(input("\nEnter your daily calorie limit: "))




if total_cal > daily_limit:
    status_msg = "⚠ Warning: You have exceeded your daily limit!"
else:
    status_msg = "✅ Good job! You are within your daily limit."




print("\n========== Daily Calorie Report ==========")
print("Meal Name\tCalories")
print("------------------------------------------")
for meal, cal in zip(meals, calories):
    print(f"{meal:<12}\t{cal}")
print("------------------------------------------")
print(f"Total:\t\t{total_cal}")
print(f"Average:\t{avg_cal:.2f}")
print("------------------------------------------")
print(status_msg)




choice = input("\nDo you want to save this session log to file? (yes/no): ").strip().lower()

if choice == "yes":
    filename = "calorie_log.txt"
    with open(filename, "w") as f:
        f.write("===== Daily Calorie Tracker Log =====\n")
        f.write(f"Timestamp: {datetime.datetime.now()}\n\n")
        f.write("Meal Name\tCalories\n")
        f.write("--------------------------------------\n")
        for meal, cal in zip(meals, calories):
            f.write(f"{meal:<12}\t{cal}\n")
        f.write("--------------------------------------\n")
        f.write(f"Total:\t\t{total_cal}\n")
        f.write(f"Average:\t{avg_cal:.2f}\n")
        f.write("--------------------------------------\n")
        f.write("status_msg ")
    print(f"\n📂 Session saved successfully to {filename}")
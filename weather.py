import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dates = ["2026-03-01", "2026-03-02", "2026-03-03", "2026-03-04", "2026-03-05",
         "2026-03-06", "2026-03-07", "2026-03-08", "2026-03-09", "2026-03-10",
         "2026-03-11", "2026-03-12", "2026-03-13", "2026-03-14", "2026-03-15",
         "2026-03-15"]
cities = [" islamabad", "ISLAMABAD ", "Islamabad", "islamabad ", " Islamabad", "ISLAMABAD",
          "Islamabad", " islamabad", "Islamabad ", "ISLAMABAD", "islamabad", " Islamabad ",
          "Islamabad", "ISLAMABAD ", "islamabad", "islamabad"]
temps = ["22C", "20C", "35C", "34C", "30C", "34C", "29C", "35C",
         "29C", "25C", "25C", "33C", "20C", "33C", "26C", "26C"]
humidity = [89, 79, np.nan, 61, 72, 52, np.nan, 48,
            55, 52, np.nan, 45, 72, 50, 66, 66]
conditions = [" Rainy", "rainy", "SUNNY", "sunny ", "Cloudy", " Sunny", "CLOUDY ", "sunny",
              "Sunny", "cloudy", " Cloudy", "SUNNY ", "RAINY", "sunny", "Cloudy ", "Cloudy "]

df = pd.DataFrame({
    "Date": dates,
    "City": cities,
    "Temperature": temps,
    "Humidity": humidity,
    "Condition": conditions
})

df["City"] = df["City"].str.strip().str.title()
df["Condition"] = df["Condition"].str.strip().str.title()
df["Temperature"] = df["Temperature"].str.replace("C", "", regex=False).astype(float)
df["Date"] = pd.to_datetime(df["Date"])

df = df.drop_duplicates()
print("Rows after dropping duplicates:", df.shape[0])

median_humidity = df["Humidity"].median()
df["Humidity"] = df["Humidity"].fillna(median_humidity)
print("Missing Humidity filled with median:", median_humidity)

corr = df["Temperature"].corr(df["Humidity"])
print("Correlation (Temperature, Humidity):", round(corr, 2))

encoded = pd.get_dummies(df, columns=["Condition"], dtype=int)
print(encoded.filter(like="Condition_").head())

condition_counts = df["Condition"].value_counts()
print("Condition counts:")
print(condition_counts)

fig, axes = plt.subplots(2, 2, figsize=(12, 9))

axes[0, 0].plot(df["Date"], df["Temperature"], marker="o", color="steelblue")
axes[0, 0].set_title("Temperature Over Time")
axes[0, 0].set_xlabel("Date")
axes[0, 0].set_ylabel("Temperature (C)")
axes[0, 0].tick_params(axis="x", rotation=45)

axes[0, 1].scatter(df["Temperature"], df["Humidity"], color="darkorange", s=60)
axes[0, 1].set_title("Temperature vs. Humidity")
axes[0, 1].set_xlabel("Temperature (C)")
axes[0, 1].set_ylabel("Humidity (%)")

axes[1, 0].pie(condition_counts.values, labels=condition_counts.index,
               autopct="%1.1f%%", startangle=90,
               colors=["#F58518", "#4C78A8", "#54A24B"])
axes[1, 0].set_title("Days by Condition")

axes[1, 1].hist(df["Temperature"], bins=5, color="seagreen", edgecolor="white")
axes[1, 1].set_title("Temperature Distribution")
axes[1, 1].set_xlabel("Temperature (C)")
axes[1, 1].set_ylabel("Number of Days")

fig.suptitle("Weather Overview", fontsize=16)
plt.tight_layout()
plt.savefig("weather_dashboard.png")
print("Saved weather_dashboard.png")
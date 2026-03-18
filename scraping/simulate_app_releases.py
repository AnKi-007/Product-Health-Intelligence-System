import pandas as pd

# Simulated release cadence (every 8 weeks)
base_date = pd.Timestamp("2025-01-01")

rows = []
for i in range(8):
    rows.append({
        "version": f"2025.{i+1}",
        "release_date": base_date + pd.DateOffset(weeks=8 * i),
        "release_notes": "Simulated production release",
        "source": "simulated"
    })

df = pd.DataFrame(rows)

df.to_csv("data/product_releases_raw.csv", index=False)

print("Simulated releases created:", len(df))
print(df)

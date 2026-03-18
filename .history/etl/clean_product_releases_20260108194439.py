import pandas as pd

df = pd.read_csv("data/product_releases_raw.csv")

df["release_date"] = pd.to_datetime(df["release_date"])

df_clean = df[
    ["version", "release_date", "release_notes", "source"]
].copy()

df_clean.to_csv("data/product_releases_clean.csv", index=False)

print("Cleaned releases:", len(df_clean))
print(df_clean.head())

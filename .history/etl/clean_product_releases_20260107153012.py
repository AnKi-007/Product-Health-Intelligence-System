import pandas as pd

# Load raw product releases
df = pd.read_csv("data/product_releases_raw.csv")

# Keep relevant columns
df_clean = df[
    [
        "version",
        "release_date",
        "release_notes",
        "source"
    ]
].copy()

# Convert release_date to datetime
df_clean["release_date"] = pd.to_datetime(df_clean["release_date"], errors="coerce")

# Normalize text
df_clean["release_notes"] = (
    df_clean["release_notes"]
    .fillna("")
    .str.replace("\n", " ", regex=False)
    .str.strip()
)

print("Cleaned product releases preview:")
print(df_clean.head())
print("\nRows after cleaning:", len(df_clean))
print("Columns:", list(df_clean.columns))

# Save cleaned version
df_clean.to_csv("data/product_releases_clean.csv", index=False)

import pandas as pd

# Load raw scraped reviews
df = pd.read_csv("data/app_reviews_raw.csv")

# Select relevant columns
df_clean = df[
    [
        "review_id",
        "review_text",
        "rating",
        "review_date",
        "likes"
    ]
].copy()

# Convert date column
df_clean["review_date"] = pd.to_datetime(df_clean["review_date"])

# Clean review text
df_clean["review_text"] = (
    df_clean["review_text"]
    .astype(str)
    .str.strip()
)

# Basic validation
print("Cleaned app reviews preview:")
print(df_clean.head())

print("Rows after cleaning:", len(df_clean))
print("Columns:", list(df_clean.columns))

import pandas as pd

# Load Spotify history CSV
file_path = "data/spotify_history.csv"
df = pd.read_csv(file_path)

# Basic checks
print("Data loaded successfully")
print("Rows:", df.shape[0])
print("Columns:", list(df.columns))

print("\nFirst 5 rows:")
print(df.head())

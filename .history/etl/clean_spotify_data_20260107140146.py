import pandas as pd

# Load raw Spotify data
df = pd.read_csv("data/spotify_history.csv")

# Select only useful columns
df_clean = df[[
    "spotify_track_uri",
    "ts",
    "platform",
    "ms_played",
    "skipped"
]]

# Rename columns to product analytics format
df_clean = df_clean.rename(columns={
    "spotify_track_uri": "feature",
    "ts": "timestamp",
    "platform": "platform",
    "ms_played": "session_duration",
    "skipped": "skipped"
})

# Convert timestamp to datetime
df_clean["timestamp"] = pd.to_datetime(df_clean["timestamp"])

# Convert ms to seconds (cleaner for analysis)
df_clean["session_duration"] = df_clean["session_duration"] / 1000

# Add user_id (simulated – acceptable for this project)
df_clean["user_id"] = "spotify_user_1"

# Reorder columns
df_clean = df_clean[
    ["user_id", "feature", "timestamp", "platform", "session_duration", "skipped"]
]

print("Cleaned data preview:")
print(df_clean.head())
print("\nRows after cleaning:", len(df_clean))

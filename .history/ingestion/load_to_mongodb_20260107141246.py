import pandas as pd
from pymongo import MongoClient

# Load cleaned data
df = pd.read_csv("data/spotify_history.csv")

# Re-apply cleaning logic (safe & reproducible)
df = df[[
    "spotify_track_uri",
    "ts",
    "platform",
    "ms_played",
    "skipped"
]]

df = df.rename(columns={
    "spotify_track_uri": "feature",
    "ts": "timestamp",
    "platform": "platform",
    "ms_played": "session_duration"
})

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["session_duration"] = df["session_duration"] / 1000
df["user_id"] = "spotify_user_1"

df = df[
    ["user_id", "feature", "timestamp", "platform", "session_duration", "skipped"]
]

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["product_analytics"]
collection = db["usage_logs"]

# Convert DataFrame to dict and insert
records = df.to_dict(orient="records")
collection.insert_many(records)

print("Data inserted into MongoDB successfully")
print("Total records inserted:", collection.count_documents({}))

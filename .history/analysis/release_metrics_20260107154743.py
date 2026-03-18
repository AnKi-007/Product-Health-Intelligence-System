import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["product_analytics"]

releases = pd.DataFrame(list(db.product_releases.find()))

releases["release_date"] = pd.to_datetime(releases["release_date"])

# Sort by time correctly
releases = releases.sort_values("release_date")

metrics = {
    "total_releases": len(releases),
    "latest_release": releases.iloc[-1]["version"],
    "release_frequency_days": releases["release_date"].diff().dt.days.mean()
}

print("RELEASE METRICS")
for k, v in metrics.items():
    print(f"{k}: {v}")

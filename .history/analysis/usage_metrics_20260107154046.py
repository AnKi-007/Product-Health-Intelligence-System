import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["product_analytics"]

usage = pd.DataFrame(list(db.usage_logs.find()))

# Basic usage KPIs
metrics = {
    "total_sessions": len(usage),
    "avg_session_duration_sec": usage["session_duration"].mean(),
    "skip_rate": usage["skipped"].mean(),
    "unique_users": usage["user_id"].nunique(),
    "platform_breakdown": usage["platform"].value_counts().to_dict()
}

print("USAGE HEALTH METRICS")
for k, v in metrics.items():
    print(f"{k}: {v}")

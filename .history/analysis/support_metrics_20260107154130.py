import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["product_analytics"]

tickets = pd.DataFrame(list(db.support_tickets.find()))

metrics = {
    "total_tickets": len(tickets),
    "avg_resolution_time_hours": tickets["resolution_time_hours"].mean(),
    "ticket_volume_by_category": tickets["issue_category"].value_counts().to_dict(),
    "priority_distribution": tickets["priority"].value_counts().to_dict(),
    "avg_satisfaction_score": tickets["satisfaction_score"].mean()
}

print("SUPPORT HEALTH METRICS")
for k, v in metrics.items():
    print(f"{k}: {v}")

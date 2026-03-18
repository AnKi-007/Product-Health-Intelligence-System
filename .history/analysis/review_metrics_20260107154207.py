import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["product_analytics"]

reviews = pd.DataFrame(list(db.app_reviews.find()))

metrics = {
    "total_reviews": len(reviews),
    "avg_rating": reviews["rating"].mean(),
    "rating_distribution": reviews["rating"].value_counts().sort_index().to_dict(),
    "low_rating_ratio": (reviews["rating"] <= 2).mean()
}

print("APP REVIEW METRICS")
for k, v in metrics.items():
    print(f"{k}: {v}")

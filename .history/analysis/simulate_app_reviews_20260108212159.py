import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["product_analytics"]

# Load REAL reviews
reviews = pd.DataFrame(list(db.app_reviews.find()))

if reviews.empty:
    print("No real reviews found.")
    exit()

reviews["review_date"] = pd.to_datetime(reviews["review_date"])

# ⏪ SHIFT BACK 12 MONTHS
reviews["review_date"] = reviews["review_date"] - pd.DateOffset(months=12)

# Tag clearly
reviews["data_type"] = "simulated"
reviews["simulation_note"] = "Spotify reviews shifted back by 12 months"

# Save separately
db.simulated_app_reviews.delete_many({})
db.simulated_app_reviews.insert_many(reviews.to_dict("records"))

print("Simulated reviews loaded:", len(reviews))
print(
    "Simulated date range:",
    reviews["review_date"].min(),
    "→",
    reviews["review_date"].max()
)

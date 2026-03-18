import pandas as pd
import numpy as np
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["product_analytics"]

# Load REAL reviews
reviews = pd.DataFrame(list(db.app_reviews.find()))

if reviews.empty:
    print("No real reviews found.")
    exit()

reviews["review_date"] = pd.to_datetime(reviews["review_date"])

# Target simulation window
start_date = pd.Timestamp("2024-01-01")
end_date = pd.Timestamp("2026-01-31")

n_reviews = len(reviews)

# Generate random dates across full window
simulated_dates = pd.to_datetime(
    np.random.uniform(
        start_date.value,
        end_date.value,
        n_reviews
    )
)

# Assign new dates
reviews["review_date"] = simulated_dates

# Tag as simulated
reviews["data_type"] = "simulated"
reviews["simulation_note"] = "Real Spotify reviews redistributed across 2024–2026"

# Sort chronologically
reviews = reviews.sort_values("review_date")

# Save to MongoDB
db.simulated_app_reviews.drop()
db.simulated_app_reviews.insert_many(reviews.to_dict("records"))

print("Simulated reviews generated:", len(reviews))
print("Date range:",
      reviews["review_date"].min(),
      "→",
      reviews["review_date"].max())

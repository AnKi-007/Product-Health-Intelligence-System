import pandas as pd
from pymongo import MongoClient

# Load cleaned product releases
df = pd.read_csv("data/product_releases_clean.csv")

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["product_analytics"]
collection = db["product_releases"]

# Reset collection (safe for development)
collection.delete_many({})

# Insert records
records = df.to_dict(orient="records")
collection.insert_many(records)

print("Product releases inserted successfully")
print("Total records:", collection.count_documents({}))

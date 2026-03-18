import pandas as pd
from pymongo import MongoClient

# Load cleaned app reviews
df = pd.read_csv("data/app_reviews_raw.csv")

df = df[
    [
        "review_id",
        "review_text",
        "rating",
        "review_date",
        "likes"
    ]
]

df["review_date"] = pd.to_datetime(df["review_date"])

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["product_analytics"]
collection = db["app_reviews"]

# Clear existing data
collection.delete_many({})

# Insert documents
records = df.to_dict(orient="records")
collection.insert_many(records)

print("App reviews inserted into MongoDB")
print("Total records:", collection.count_documents({}))

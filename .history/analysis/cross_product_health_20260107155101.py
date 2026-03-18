import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["product_analytics"]

usage = pd.DataFrame(list(db.usage_logs.find()))
tickets = pd.DataFrame(list(db.support_tickets.find()))
reviews = pd.DataFrame(list(db.app_reviews.find()))
releases = pd.DataFrame(list(db.product_releases.find()))

print("CROSS PRODUCT HEALTH SUMMARY")
print("----------------------------------")
print("Usage sessions:", len(usage))
print("Avg session duration:", usage["session_duration"].mean())
print("Ticket volume:", len(tickets))
print("Avg ticket resolution time:", tickets["resolution_time_hours"].mean())
print("Avg app rating:", reviews["rating"].mean())
print("Total releases:", len(releases))

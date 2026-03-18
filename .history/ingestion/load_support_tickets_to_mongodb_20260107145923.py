import pandas as pd
from pymongo import MongoClient

# Load cleaned support tickets
df = pd.read_csv("data/support_tickets.csv")

# Apply same cleaning logic (safe + reproducible)
df = df[
    [
        "Ticket_ID",
        "Issue_Category",
        "Priority_Level",
        "Ticket_Channel",
        "Submission_Date",
        "Resolution_Time_Hours",
        "Assigned_Agent",
        "Satisfaction_Score"
    ]
]

df.rename(
    columns={
        "Ticket_ID": "ticket_id",
        "Issue_Category": "issue_category",
        "Priority_Level": "priority",
        "Ticket_Channel": "channel",
        "Submission_Date": "created_at",
        "Resolution_Time_Hours": "resolution_time_hours",
        "Assigned_Agent": "agent",
        "Satisfaction_Score": "satisfaction_score",
    },
    inplace=True,
)

df["created_at"] = pd.to_datetime(df["created_at"])

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["product_analytics"]
collection = db["support_tickets"]

# Clear old data (safe for dev)
collection.delete_many({})

# Insert records
records = df.to_dict(orient="records")
collection.insert_many(records)

print("Support tickets inserted into MongoDB successfully")
print("Total records:", collection.count_documents({}))

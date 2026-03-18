import pandas as pd

# Load raw support tickets
df = pd.read_csv("data/support_tickets.csv")

# Select only analytics-relevant columns
df_clean = df[
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
].copy()

# Rename columns to analytics-friendly names
df_clean.rename(
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
    inplace=True
)

# Convert date column
df_clean["created_at"] = pd.to_datetime(df_clean["created_at"])

# Basic sanity checks
print("Cleaned support tickets preview:")
print(df_clean.head())

print("\nRows after cleaning:", len(df_clean))
print("Columns:", list(df_clean.columns))

import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["product_analytics"]

releases = pd.DataFrame(list(db.product_releases.find()))
tickets = pd.DataFrame(list(db.support_tickets.find()))
reviews = pd.DataFrame(list(db.app_reviews.find()))

# Normalize timestamps
releases["release_date"] = pd.to_datetime(releases["release_date"])
tickets["created_at"] = pd.to_datetime(tickets["created_at"])
reviews["review_date"] = pd.to_datetime(reviews["review_date"])

# Focus only where reviews exist (Dec 2025 – Jan 2026)
review_start = reviews["review_date"].min()
review_end = reviews["review_date"].max()

releases = releases[
    (releases["release_date"] >= review_start) &
    (releases["release_date"] <= review_end)
].sort_values("release_date")

WINDOW_DAYS = 14
rows = []

for _, r in releases.iterrows():
    rd = r["release_date"]

    before_tickets = tickets[
        (tickets["created_at"] >= rd - pd.Timedelta(days=WINDOW_DAYS)) &
        (tickets["created_at"] < rd)
    ]

    after_tickets = tickets[
        (tickets["created_at"] >= rd) &
        (tickets["created_at"] <= rd + pd.Timedelta(days=WINDOW_DAYS))
    ]

    after_reviews = reviews[
        (reviews["review_date"] >= rd) &
        (reviews["review_date"] <= rd + pd.Timedelta(days=WINDOW_DAYS))
    ]

    if after_reviews.empty:
        continue  # cannot correlate without reviews

    rows.append({
        "version": r["version"],
        "ticket_delta": len(after_tickets) - len(before_tickets),
        "ticket_change_pct": (
            (len(after_tickets) - len(before_tickets)) /
            max(len(before_tickets), 1)
        ) * 100,
        "avg_rating_after": after_reviews["rating"].mean()
    })

corr_df = pd.DataFrame(rows)

print("\nPHASE 2 – RELEASE CORRELATION ANALYSIS\n")
print("Data points used:", len(corr_df))
print(corr_df)

if len(corr_df) < 2:
    print("\nNot enough data points for correlation.")
    exit()

print("\nCORRELATION RESULTS")
print(
    "Ticket delta vs rating:",
    round(corr_df["ticket_delta"].corr(corr_df["avg_rating_after"]), 3)
)
print(
    "Ticket % change vs rating:",
    round(corr_df["ticket_change_pct"].corr(corr_df["avg_rating_after"]), 3)
)

print("\nAnalysis complete.")

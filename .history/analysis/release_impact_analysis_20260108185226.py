import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["product_analytics"]

releases = pd.DataFrame(list(db.product_releases.find()))
tickets = pd.DataFrame(list(db.support_tickets.find()))
reviews = pd.DataFrame(list(db.app_reviews.find()))

# Normalize timestamps
releases["release_date"] = pd.to_datetime(releases["release_date"], utc=True).dt.tz_localize(None)
tickets["created_at"] = pd.to_datetime(tickets["created_at"]).dt.tz_localize(None)
reviews["review_date"] = pd.to_datetime(reviews["review_date"]).dt.tz_localize(None)

releases = releases.sort_values("release_date")

WINDOW_DAYS = 14
results = []

for _, r in releases.iterrows():
    release_date = r["release_date"]
    before_start = release_date - pd.Timedelta(days=WINDOW_DAYS)
    after_end = release_date + pd.Timedelta(days=WINDOW_DAYS)

    tickets_before = tickets[
        (tickets["created_at"] >= before_start) &
        (tickets["created_at"] < release_date)
    ]

    tickets_after = tickets[
        (tickets["created_at"] >= release_date) &
        (tickets["created_at"] <= after_end)
    ]

    reviews_before = reviews[
        (reviews["review_date"] >= before_start) &
        (reviews["review_date"] < release_date)
    ]

    reviews_after = reviews[
        (reviews["review_date"] >= release_date) &
        (reviews["review_date"] <= after_end)
    ]

    results.append({
        "version": r["version"],
        "release_date": release_date,
        "tickets_before": len(tickets_before),
        "tickets_after": len(tickets_after),
        "ticket_change_pct": (
            (len(tickets_after) - len(tickets_before)) /
            max(len(tickets_before), 1)
        ) * 100,
        "avg_rating_before": reviews_before["rating"].mean(),
        "avg_rating_after": reviews_after["rating"].mean()
    })

impact_df = pd.DataFrame(results)

print("RELEASE IMPACT ANALYSIS")
print(impact_df.head())

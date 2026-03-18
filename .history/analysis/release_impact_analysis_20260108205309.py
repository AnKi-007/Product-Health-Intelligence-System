import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["product_analytics"]

releases = pd.DataFrame(list(db.product_releases.find()))
tickets = pd.DataFrame(list(db.support_tickets.find()))
reviews = pd.DataFrame(list(db.app_reviews.find()))

# -----------------------------
# Normalize timestamps
# -----------------------------
releases["release_date"] = pd.to_datetime(
    releases["release_date"], utc=True
).dt.tz_localize(None)

tickets["created_at"] = pd.to_datetime(
    tickets["created_at"]
).dt.tz_localize(None)

reviews["review_date"] = pd.to_datetime(
    reviews["review_date"]
).dt.tz_localize(None)

releases = releases.sort_values("release_date")

print("\nDATA COVERAGE")
print("Reviews:", reviews["review_date"].min(), "→", reviews["review_date"].max())
print("Tickets:", tickets["created_at"].min(), "→", tickets["created_at"].max())
print("Releases:", releases["release_date"].min(), "→", releases["release_date"].max())

# WINDOWS
TICKET_WINDOW_DAYS = 14
REVIEW_WINDOW_DAYS = 30

results = []

for _, r in releases.iterrows():
    release_date = r["release_date"]

    # Ticket windows
    ticket_before_start = release_date - pd.Timedelta(days=TICKET_WINDOW_DAYS)
    ticket_after_end = release_date + pd.Timedelta(days=TICKET_WINDOW_DAYS)

    tickets_before = tickets[
        (tickets["created_at"] >= ticket_before_start) &
        (tickets["created_at"] < release_date)
    ]

    tickets_after = tickets[
        (tickets["created_at"] >= release_date) &
        (tickets["created_at"] <= ticket_after_end)
    ]

    # Reviews ONLY if they exist after release
    review_after_end = release_date + pd.Timedelta(days=REVIEW_WINDOW_DAYS)

    reviews_after = reviews[
        (reviews["review_date"] >= release_date) &
        (reviews["review_date"] <= review_after_end)
    ]

    results.append({
        "version": r["version"],
        "release_date": release_date.date(),
        "tickets_before": len(tickets_before),
        "tickets_after": len(tickets_after),
        "ticket_change_pct": (
            (len(tickets_after) - len(tickets_before)) /
            max(len(tickets_before), 1)
        ) * 100,
        "avg_rating_after": (
            round(reviews_after["rating"].mean(), 2)
            if len(reviews_after) >= 10 else "Not observable"
        ),
        "reviews_after_count": len(reviews_after)
    })

impact_df = pd.DataFrame(results)

print("\nRELEASE IMPACT ANALYSIS (FINAL)")
print(impact_df)
print("\nAnalysis complete.")

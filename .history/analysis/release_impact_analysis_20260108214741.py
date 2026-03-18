import pandas as pd
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["product_analytics"]

releases = pd.DataFrame(list(db.product_releases.find()))
tickets = pd.DataFrame(list(db.support_tickets.find()))
reviews = pd.DataFrame(list(db.simulated_app_reviews.find()))

# Safety checks
if releases.empty or tickets.empty or reviews.empty:
    print("ERROR: One or more required datasets are empty.")
    exit()

# Normalize timestamps
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

# Data coverage logging
print("\nDATA COVERAGE")
print("Reviews:", reviews["review_date"].min(), "→", reviews["review_date"].max())
print("Tickets:", tickets["created_at"].min(), "→", tickets["created_at"].max())
print("Releases:", releases["release_date"].min(), "→", releases["release_date"].max())

# Time-aligned release filtering
min_ticket_date = tickets["created_at"].min()
max_review_date = reviews["review_date"].max()

releases = releases[
    (releases["release_date"] >= min_ticket_date) &
    (releases["release_date"] <= max_review_date)
]

print("\nRELEASE IMPACT ANALYSIS")
print("Filtered releases count:", len(releases))

if releases.empty:
    print("No overlapping releases. Analysis stopped.")
    exit()

# Analysis windows
TICKET_WINDOW_DAYS = 14
REVIEW_WINDOW_DAYS = 30

results = []

# Core impact loop
for _, r in releases.iterrows():
    release_date = r["release_date"]

    ticket_before_start = release_date - pd.Timedelta(days=TICKET_WINDOW_DAYS)
    ticket_after_end = release_date + pd.Timedelta(days=TICKET_WINDOW_DAYS)

    review_after_end = release_date + pd.Timedelta(days=REVIEW_WINDOW_DAYS)

    tickets_before = tickets[
        (tickets["created_at"] >= ticket_before_start) &
        (tickets["created_at"] < release_date)
    ]

    tickets_after = tickets[
        (tickets["created_at"] >= release_date) &
        (tickets["created_at"] <= ticket_after_end)
    ]

    reviews_after = reviews[
        (reviews["review_date"] >= release_date) &
        (reviews["review_date"] <= review_after_end)
    ]

    avg_rating_after = (
        round(reviews_after["rating"].mean(), 2)
        if len(reviews_after) >= 10
        else "Not observable"
    )

    results.append({
        "version": r["version"],
        "release_date": release_date,
        "tickets_before": len(tickets_before),
        "tickets_after": len(tickets_after),
        "ticket_change_pct": round(
            ((len(tickets_after) - len(tickets_before)) /
             max(len(tickets_before), 1)) * 100, 2
        ),
        "avg_rating_after": avg_rating_after,
        "reviews_after_count": len(reviews_after)
    })

# Final DataFrames
impact_df = pd.DataFrame(results)

print("\nRELEASE IMPACT ANALYSIS (ALL RELEASES)")
print(impact_df)

# FILTER
strict_impact_df = impact_df[
    (impact_df["tickets_before"] > 0) &
    (impact_df["reviews_after_count"] >= 50)
].copy()

print("\nRELEASE IMPACT ANALYSIS (STRICT SIGNALS ONLY)")
print("Releases used:", len(strict_impact_df))
print(strict_impact_df)

# Save outputs for Phase 2
impact_df.to_csv("data/release_impact_full.csv", index=False)
strict_impact_df.to_csv("data/release_impact_strict.csv", index=False)

print("\nAnalysis complete.")

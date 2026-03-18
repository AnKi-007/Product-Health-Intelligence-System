import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["product_analytics"]

impact_df = pd.DataFrame(list(db.release_impact.find()))

print("\nPHASE 2: RELEASE CORRELATION ANALYSIS\n")

# Keep only rows with observable ratings
corr_df = impact_df[
    (impact_df["avg_rating_after"] != "Not observable") &
    (impact_df["avg_rating_before"] != "Not observable")
].copy()

if corr_df.empty:
    print("Not enough overlapping data for correlation.")
    exit()

# Convert rating columns
corr_df["avg_rating_before"] = corr_df["avg_rating_before"].astype(float)
corr_df["avg_rating_after"] = corr_df["avg_rating_after"].astype(float)

# Derived metrics
corr_df["ticket_delta"] = corr_df["tickets_after"] - corr_df["tickets_before"]
corr_df["rating_delta"] = (
    corr_df["avg_rating_after"] - corr_df["avg_rating_before"]
)

print("Data points used:", len(corr_df))
print("\nDerived metrics preview:")
print(corr_df[
    ["version", "ticket_delta", "ticket_change_pct", "rating_delta"]
])

# Correlations
ticket_vs_rating = corr_df["ticket_delta"].corr(corr_df["rating_delta"])
ticket_pct_vs_rating = corr_df["ticket_change_pct"].corr(corr_df["rating_delta"])

print("\nCORRELATION RESULTS")
print("Ticket delta vs rating delta:", round(ticket_vs_rating, 3))
print("Ticket % change vs rating delta:", round(ticket_pct_vs_rating, 3))

# Risk flagging
corr_df["risk_flag"] = (
    (corr_df["ticket_change_pct"] > 10) &
    (corr_df["rating_delta"] < 0)
)

print("\nHIGH-RISK RELEASES")
print(corr_df[corr_df["risk_flag"]][
    ["version", "ticket_change_pct", "rating_delta"]
])

print("\nPhase 2 complete.")

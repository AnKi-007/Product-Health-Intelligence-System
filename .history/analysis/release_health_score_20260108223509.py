import pandas as pd
import numpy as np

print("\nRELEASE HEALTH SCORE\n")


# Load strict impact data
impact_df = pd.read_csv("data/release_impact_strict.csv")

if impact_df.empty:
    print("ERROR: No impact data found.")
    exit()

# Ensure numeric types
impact_df["ticket_change_pct"] = pd.to_numeric(
    impact_df["ticket_change_pct"], errors="coerce"
)

impact_df["avg_rating_after"] = pd.to_numeric(
    impact_df["avg_rating_after"], errors="coerce"
)

impact_df["reviews_after_count"] = pd.to_numeric(
    impact_df["reviews_after_count"], errors="coerce"
)

# Drop invalid rows
impact_df = impact_df.dropna(
    subset=["ticket_change_pct", "avg_rating_after", "reviews_after_count"]
)

print("Releases evaluated:", len(impact_df))

# Normalization helpers
def normalize(series):
    return (series - series.min()) / (series.max() - series.min())

impact_df["rating_norm"] = normalize(impact_df["avg_rating_after"])
impact_df["ticket_norm"] = normalize(impact_df["ticket_change_pct"])
impact_df["review_confidence"] = normalize(
    np.log1p(impact_df["reviews_after_count"])
)

# Health Score Formula
impact_df["release_health_score"] = (
    (impact_df["rating_norm"] * 0.5)
    - (impact_df["ticket_norm"] * 0.3)
    + (impact_df["review_confidence"] * 0.2)
)

# Rank releases
impact_df = impact_df.sort_values(
    "release_health_score", ascending=False
)

impact_df["health_rank"] = range(1, len(impact_df) + 1)

# Output
columns = [
    "health_rank",
    "version",
    "ticket_change_pct",
    "avg_rating_after",
    "reviews_after_count",
    "release_health_score",
]

print("\nRELEASE HEALTH SCORES\n")
print(
    impact_df[columns].round(3)
)

# Save results
impact_df.to_csv(
    "data/release_health_scores.csv",
    index=False
)

print("\nSaved → data/release_health_scores.csv")
print("\nPhase 3 complete.")

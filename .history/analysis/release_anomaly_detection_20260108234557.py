import pandas as pd
from sklearn.ensemble import IsolationForest

print("\nPHASE 4 — RELEASE ANOMALY DETECTION")

# Load release health scores (output of previous phase)
impact_df = pd.read_csv("data/release_health_scores.csv")

if impact_df.empty:
    print("ERROR: No release health scores found.")
    exit()

print("\nInput releases:", len(impact_df))

# Select features for anomaly detection
features = [
    "ticket_change_pct",
    "avg_rating_after",
    "reviews_after_count",
    "release_health_score",
]

X = impact_df[features].copy()

# Ensure numeric
X = X.apply(pd.to_numeric, errors="coerce")

# Drop rows with missing values
valid_idx = X.dropna().index
X = X.loc[valid_idx]
impact_df = impact_df.loc[valid_idx]

print("Valid releases for anomaly detection:", len(X))

if len(X) < 3:
    print("Not enough data for anomaly detection.")
    exit()

# Train Isolation Forest
model = IsolationForest(
    n_estimators=200,
    contamination=0.15,   # assume ~15% releases can be unusual
    random_state=42
)

impact_df["anomaly_score"] = model.fit_predict(X)
impact_df["is_anomaly"] = impact_df["anomaly_score"].apply(
    lambda x: "Yes" if x == -1 else "No"
)

# Show results
print("\nANOMALY DETECTION RESULTS\n")

print(
    impact_df[
        [
            "version",
            "ticket_change_pct",
            "avg_rating_after",
            "reviews_after_count",
            "release_health_score",
            "is_anomaly",
        ]
    ].round(3)
)

# Save results
impact_df.to_csv("data/release_anomaly_analysis.csv", index=False)

print("\nSaved → data/release_anomaly_analysis.csv")
print("Phase 4 complete.")

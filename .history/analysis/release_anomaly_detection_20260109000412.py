import pandas as pd
from sklearn.ensemble import IsolationForest

print("\nPHASE 4 — RELEASE ANOMALY DETECTION")

# -------------------------------------------------
# Load release health scores (output of previous phase)
# -------------------------------------------------
impact_df = pd.read_csv("data/release_health_scores.csv")

if impact_df.empty:
    print("ERROR: No release health scores found.")
    exit()

print("Input releases:", len(impact_df))

# -------------------------------------------------
# Select features for anomaly detection
# -------------------------------------------------
features = [
    "ticket_change_pct",
    "avg_rating_after",
    "reviews_after_count",
    "release_health_score"
]

X = impact_df[features].copy()
X = X.apply(pd.to_numeric, errors="coerce")

# Drop rows with missing values
valid_idx = X.dropna().index
X = X.loc[valid_idx]
impact_df = impact_df.loc[valid_idx]

print("Valid releases for anomaly detection:", len(X))

if len(X) < 3:
    print("Not enough data for anomaly detection.")
    exit()

# -------------------------------------------------
# Train Isolation Forest (unsupervised)
# -------------------------------------------------
model = IsolationForest(
    n_estimators=200,
    contamination=0.15,
    random_state=42
)

model.fit(X)

# -------------------------------------------------
# Generate anomaly scores
# -------------------------------------------------
impact_df["anomaly_score"] = model.decision_function(X)
impact_df["anomaly_flag"] = model.predict(X)

impact_df["is_anomaly"] = impact_df["anomaly_flag"].apply(
    lambda x: "Yes" if x == -1 else "No"
)

# Rank anomalies (lowest score = most anomalous)
impact_df["anomaly_rank"] = impact_df["anomaly_score"].rank(
    method="dense"
)

# -------------------------------------------------
# Business validation signals (KEY PART)
# -------------------------------------------------
impact_df["low_rating_flag"] = impact_df["avg_rating_after"] < 4.0
impact_df["ticket_spike_flag"] = impact_df["ticket_change_pct"] > 10
impact_df["low_health_flag"] = impact_df["release_health_score"] < 0

# -------------------------------------------------
# Output
# -------------------------------------------------
columns = [
    "version",
    "ticket_change_pct",
    "avg_rating_after",
    "reviews_after_count",
    "release_health_score",
    "anomaly_score",
    "anomaly_rank",
    "is_anomaly",
    "low_rating_flag",
    "ticket_spike_flag",
    "low_health_flag"
]

print("\nANOMALY DETECTION RESULTS")
print(impact_df[columns].sort_values("anomaly_score").round(3))

# Save for next phase (LLM + reporting)
impact_df.to_csv("data/release_anomaly_analysis.csv", index=False)

print("\nSaved → data/release_anomaly_analysis.csv")
print("Phase 4 complete.")

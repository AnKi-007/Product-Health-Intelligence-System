import pandas as pd
from sklearn.ensemble import IsolationForest

print("\nPHASE 4 — RELEASE ANOMALY DETECTION\n")

# Load input data (output of health score phase)
impact_df = pd.read_csv("data/release_health_scores.csv")

if impact_df.empty:
    print("ERROR: No release health scores found.")
    exit()

print("Input releases:", len(impact_df))

# Select features for anomaly detection (ML)
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

# Train Isolation Forest (unsupervised ML)
iso = IsolationForest(
    n_estimators=200,
    contamination=0.15,
    random_state=42,
)

iso.fit(X)

# Generate anomaly scores
impact_df["anomaly_score"] = iso.decision_function(X)
impact_df["anomaly_rank"] = impact_df["anomaly_score"].rank(ascending=True)

impact_df["is_anomaly"] = iso.predict(X)
impact_df["is_anomaly"] = impact_df["is_anomaly"].map({-1: "Yes", 1: "No"})

# BUSINESS VALIDATION SIGNALS (RULE-BASED)
impact_df["low_rating_flag"] = impact_df["avg_rating_after"] < 4.0
impact_df["ticket_spike_flag"] = impact_df["ticket_change_pct"] > 10
impact_df["low_health_flag"] = impact_df["release_health_score"] < 0

# Business risk score
impact_df["business_risk"] = (
    impact_df["low_rating_flag"].astype(int)
    + impact_df["ticket_spike_flag"].astype(int)
    + impact_df["low_health_flag"].astype(int)
)

impact_df["risk_level"] = impact_df["business_risk"].apply(
    lambda x: "High" if x >= 2 else "Medium" if x == 1 else "Low"
)

# Final Output
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
    "low_health_flag",
    "business_risk",
    "risk_level",
]

print("\nANOMALY DETECTION RESULTS\n")
print(impact_df[columns].sort_values("anomaly_rank").round(3))

# Save results
impact_df[columns].to_csv(
    "data/release_anomaly_analysis.csv", index=False
)

print("\nSaved → data/release_anomaly_analysis.csv")
print("Phase 4 complete.")

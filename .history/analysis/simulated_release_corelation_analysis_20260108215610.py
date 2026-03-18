import pandas as pd

print("\nSIMULATED RELEASE CORRELATION ANALYSIS")

# -------------------------------
# Load strict impact data
# -------------------------------
impact_df = pd.read_csv("data/release_impact_strict.csv")

if impact_df.empty:
    print("ERROR: No valid release impact data found.")
    exit()

print("\nInput data points:", len(impact_df))
print(impact_df[[
    "version",
    "ticket_change_pct",
    "avg_rating_after",
    "reviews_after_count"
]])

# -------------------------------
# Prepare correlation-safe columns
# -------------------------------
impact_df["avg_rating_after"] = pd.to_numeric(
    impact_df["avg_rating_after"], errors="coerce"
)

impact_df["ticket_change_pct"] = pd.to_numeric(
    impact_df["ticket_change_pct"], errors="coerce"
)

corr_df = impact_df.dropna(
    subset=["ticket_change_pct", "avg_rating_after"]
)

print("\nValid data points for correlation:", len(corr_df))

if len(corr_df) < 2:
    print("Not enough data points for correlation.")
    exit()

# -------------------------------
# Correlation calculations
# -------------------------------
ticket_vs_rating = corr_df["ticket_change_pct"].corr(
    corr_df["avg_rating_after"]
)

# -------------------------------
# Output results
# -------------------------------
print("\nCORRELATION RESULTS")
print("--------------------------------")
print(
    "Ticket % change vs Avg rating after:",
    round(ticket_vs_rating, 3)
)

print("\nInterpretation:")
if ticket_vs_rating > 0.3:
    print("- Strong positive relationship")
elif ticket_vs_rating < -0.3:
    print("- Strong negative relationship")
else:
    print("- Weak or no linear relationship")

print("\nAnalysis complete.")

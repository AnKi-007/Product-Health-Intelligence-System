import pandas as pd
from pathlib import Path

REPORT_PATH = Path("reports/monthly_product_health_report.md")

health_df = pd.read_csv("data/release_health_scores.csv")
anomaly_df = pd.read_csv("data/release_anomaly_analysis.csv")

high_risk = anomaly_df[anomaly_df["risk_level"] == "High"]
medium_risk = anomaly_df[anomaly_df["risk_level"] == "Medium"]

best_release = health_df.sort_values(
    "release_health_score", ascending=False
).iloc[0]

worst_release = health_df.sort_values(
    "release_health_score"
).iloc[0]

with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write("# Monthly Product Health Report — January 2026\n\n")

    f.write("## Executive Summary\n")
    f.write(
        f"This report evaluates {len(health_df)} product releases using "
        "support ticket trends, user ratings, machine learning–based anomaly "
        "detection, and LLM-generated explanations.\n\n"
    )

    f.write(f"- High-risk releases: {len(high_risk)}\n")
    f.write(f"- Medium-risk releases: {len(medium_risk)}\n")
    f.write(f"- Best release: {best_release['version']}\n")
    f.write(f"- Worst release: {worst_release['version']}\n\n")

    f.write("## Release Health Scores\n")
    for _, row in health_df.iterrows():
        f.write(
            f"- Version {row['version']}: "
            f"Health Score {round(row['release_health_score'], 3)}\n"
        )

    f.write("\n## Anomaly Detection Summary\n")
    if high_risk.empty:
        f.write("No high-risk anomalies detected.\n")
    else:
        for _, row in high_risk.iterrows():
            f.write(
                f"- Version {row['version']} flagged as HIGH RISK "
                f"(ticket change {round(row['ticket_change_pct'], 2)}%, "
                f"avg rating {round(row['avg_rating_after'], 2)})\n"
            )

    f.write("\n## Interpretation\n")
    f.write(
        "Anomalies were detected using an Isolation Forest model applied "
        "to post-release behavioral signals. These findings are validated "
        "using business rules and downstream impact indicators.\n"
    )

    f.write("\n## Recommendations\n")
    if not high_risk.empty:
        f.write(
            "- Investigate high-risk releases immediately\n"
            "- Review user feedback for recurring complaints\n"
            "- Prioritize stabilization or rollback if necessary\n"
        )
    else:
        f.write(
            "- Continue monitoring releases\n"
            "- No immediate intervention required\n"
        )

    f.write("\n## Conclusion\n")
    f.write(
        "This automated Product Health Intelligence System enables "
        "monthly monitoring of product releases by combining structured "
        "data analysis, machine learning, and explainable AI insights.\n"
    )

print("Monthly product health report generated successfully.")

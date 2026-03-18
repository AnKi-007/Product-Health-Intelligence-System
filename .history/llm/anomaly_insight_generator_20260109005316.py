import os
import pandas as pd
from openai import OpenAI

print("\nPHASE 5 — LLM ANOMALY INSIGHT GENERATION\n")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if not os.getenv("OPENAI_API_KEY"):
    print("ERROR: OPENAI_API_KEY not set.")
    exit()

# Load anomaly analysis output
df = pd.read_csv("data/release_anomaly_analysis.csv")

if df.empty:
    print("ERROR: No anomaly data found.")
    exit()

# Focus only on anomalies
anomalies = df[df["is_anomaly"] == "Yes"]

if anomalies.empty:
    print("No anomalies detected. Nothing to explain.")
    exit()

print(f"Anomalies found: {len(anomalies)}\n")

insights = []

# Generate LLM explanations
for _, row in anomalies.iterrows():

    prompt = f"""
You are a senior product analytics assistant.

Explain the following anomalous product release in clear, business-friendly language.

Release version: {row['version']}
Ticket change percent: {row['ticket_change_pct']}%
Average rating after release: {row['avg_rating_after']}
Number of reviews after release: {row['reviews_after_count']}
Health score: {row['release_health_score']}
Business risk level: {row['risk_level']}

Explain:
1. What likely went wrong
2. Why this release is risky
3. What the product team should investigate next

Keep the explanation concise and professional.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    explanation = response.choices[0].message.content.strip()

    insights.append({
        "version": row["version"],
        "risk_level": row["risk_level"],
        "llm_explanation": explanation
    })

# Save insights
insights_df = pd.DataFrame(insights)
insights_df.to_csv(
    "reports/release_anomaly_llm_insights.csv",
    index=False
)

print("LLM anomaly insights generated successfully.")
print("Saved → reports/release_anomaly_llm_insights.csv")
print("\nPhase 5 complete.")

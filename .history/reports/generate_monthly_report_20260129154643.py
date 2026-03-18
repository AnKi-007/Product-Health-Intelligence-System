"""
PHASE 5 — LLM ANOMALY INSIGHT GENERATION

Purpose:
Generate human-readable explanations for anomalous releases.
If LLM API is unavailable, fall back to rule-based explanations.
"""

import pandas as pd
from pathlib import Path

try:
    from openai import OpenAI, RateLimitError
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False

# CONFIG

RUN_LLM = True  # set False if you want to disable LLM completely
MODEL_NAME = "gpt-4o-mini"

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "release_anomaly_analysis.csv"
OUTPUT_PATH = BASE_DIR / "reports" / "release_anomaly_llm_insights.csv"

# LOAD DATA

print("\nPHASE 5 — LLM ANOMALY INSIGHT GENERATION\n")

df = pd.read_csv(DATA_PATH)

anomalies = df[df["is_anomaly"] == True].copy()

print("Anomalies found:", len(anomalies))

if anomalies.empty:
    print("No anomalies to explain.")
    anomalies["llm_explanation"] = []
    anomalies.to_csv(OUTPUT_PATH, index=False)
    print("Phase 5 complete.")
    exit()

# LLM CLIENT

client = None
if RUN_LLM and OPENAI_AVAILABLE:
    try:
        client = OpenAI()
    except Exception:
        client = None

# FALLBACK EXPLANATION (BUSINESS SAFE)

def fallback_explanation(row):
    reasons = []

    if row["ticket_spike_flag"]:
        reasons.append("significant increase in support tickets")

    if row["low_health_flag"]:
        reasons.append("low overall release health score")

    if row["avg_rating_after"] < 3.8:
        reasons.append("below-average user ratings")

    if not reasons:
        reasons.append("unusual metric combination detected")

    return (
        f"Release {row['version']} was flagged as anomalous due to "
        + ", ".join(reasons)
        + ". Manual investigation is recommended."
    )

# LLM PROMPT

def build_prompt(row):
    return f"""
A product release has been flagged as anomalous.

Release version: {row['version']}
Ticket change percentage: {row['ticket_change_pct']:.2f}%
Average rating after release: {row['avg_rating_after']:.2f}
Review volume: {row['reviews_after_count']}
Overall health score: {row['release_health_score']:.3f}
Risk level: {row['risk_level']}

Explain in simple business language:
- What likely went wrong
- Why this release is risky
- What teams should investigate
"""

# GENERATE INSIGHTS

explanations = []

for _, row in anomalies.iterrows():
    explanation = None

    if RUN_LLM and client is not None:
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a senior product analytics expert."},
                    {"role": "user", "content": build_prompt(row)}
                ],
                temperature=0.2
            )
            explanation = response.choices[0].message.content.strip()

        except RateLimitError:
            explanation = fallback_explanation(row)

        except Exception:
            explanation = fallback_explanation(row)
    else:
        explanation = fallback_explanation(row)

    explanations.append(explanation)

anomalies["llm_explanation"] = explanations

# SAVE OUTPUT

anomalies.to_csv(OUTPUT_PATH, index=False)

print("LLM insights generated successfully.")
print(f"Saved → {OUTPUT_PATH}")
print("Phase 5 complete.")

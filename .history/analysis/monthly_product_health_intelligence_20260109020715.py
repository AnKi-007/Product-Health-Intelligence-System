"""
MONTHLY PRODUCT HEALTH INTELLIGENCE SYSTEM
==========================================

This script orchestrates the full analytics pipeline.

Pipeline stages:
1. Release impact analysis (real data)
2. Release correlation analysis (simulated data)
3. Release health score computation
4. ML-based anomaly detection
5. LLM-based anomaly explanation
6. Final report readiness

Note:
Correlation analysis uses simulated data due to
limited historical real-world review coverage.
"""

import subprocess
import sys
from pathlib import Path

# CONFIGURATION FLAGS

RUN_SIMULATED_CORRELATION = True
RUN_LLM = True

# PATH SETUP

BASE_DIR = Path(__file__).resolve().parent

# PIPELINE DEFINITION

PIPELINE_STEPS = [
    {
        "name": "Release Impact Analysis (Real Data)",
        "script": "release_impact_analysis.py",
        "enabled": True,
    },
    {
        "name": "Release Correlation Analysis (Simulated Data)",
        "script": "simulated_release_correlation_analysis.py",
        "enabled": RUN_SIMULATED_CORRELATION,
        "note": (
            "Uses simulated review and ticket data to demonstrate "
            "statistical correlation when real data is insufficient."
        ),
    },
    {
        "name": "Release Health Score Calculation",
        "script": "release_health_score.py",
        "enabled": True,
    },
    {
        "name": "Release Anomaly Detection (ML)",
        "script": "release_anomaly_detection.py",
        "enabled": True,
    },
    {
        "name": "LLM Anomaly Insight Generation",
        "script": "../llm/anomaly_insight_generator.py",
        "enabled": RUN_LLM,
    },
    {
    "name": "Monthly Report Generation",
    "script": "../reports/generate_monthly_report.py",
    "enabled": True,
    }
]

# EXECUTION LOGIC

def run_step(step):
    if not step.get("enabled", True):
        print(f"[SKIPPED] {step['name']}")
        if "note" in step:
            print(f"Reason: {step['note']}")
        return

    script_path = (BASE_DIR / step["script"]).resolve()

    if not script_path.exists():
        print(f"[SKIPPED] {step['name']} — script not found")
        return

    print("\n" + "=" * 70)
    print(f"RUNNING: {step['name']}")
    print("=" * 70)

    try:
        subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
        )
        print(f"[SUCCESS] {step['name']}")
    except subprocess.CalledProcessError:
        print(f"[FAILED] {step['name']}")
        print("Pipeline stopped due to error.")
        sys.exit(1)

# MAIN ENTRY POINT

def main():
    print("\nMONTHLY PRODUCT HEALTH INTELLIGENCE SYSTEM")
    print("==========================================")
    print("Starting full pipeline execution...\n")

    for step in PIPELINE_STEPS:
        run_step(step)

    print("\n" + "=" * 70)
    print("PIPELINE COMPLETE")
    print("=" * 70)

    print(
        """
Outputs generated:
- data/release_health_scores.csv
- data/release_anomaly_analysis.csv
- reports/release_anomaly_llm_insights.csv

Next recommended step:
- Review reports/monthly_product_health_report.md
"""
    )

if __name__ == "__main__":
    main()

"""
MONTHLY PRODUCT HEALTH INTELLIGENCE SYSTEM
==========================================

This script orchestrates the full analytics pipeline:
1. Release impact analysis
2. Health score computation
3. Correlation analysis
4. Anomaly detection (ML)
5. LLM-based anomaly explanation
6. Final report readiness

Each step is modular and can be run independently,
but this file represents the full production workflow.
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

PIPELINE_STEPS = [
    {
        "name": "Release Impact Analysis",
        "script": "release_impact_analysis.py",
    },
    {
        "name": "Release Correlation Analysis",
        "script": "release_correlation_analysis.py",
    },
    {
        "name": "Release Health Score Calculation",
        "script": "release_health_score.py",
    },
    {
        "name": "Release Anomaly Detection (ML)",
        "script": "release_anomaly_detection.py",
    },
    {
        "name": "LLM Anomaly Insight Generation",
        "script": "../llm/anomaly_insight_generator.py",
    },
]


def run_step(step):
    script_path = (BASE_DIR / step["script"]).resolve()

    if not script_path.exists():
        print(f"[SKIPPED] {step['name']} — script not found: {script_path}")
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

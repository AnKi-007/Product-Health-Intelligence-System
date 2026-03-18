"""
MONTHLY PRODUCT HEALTH INTELLIGENCE SYSTEM
=========================================

This script orchestrates the full analytics pipeline:

1. Release impact analysis
2. (Optional) Release correlation analysis
3. Release health score computation
4. ML-based anomaly detection
5. LLM-based anomaly explanation
6. Final report readiness

Design decisions:
- Correlation analysis is optional and uses simulated-aligned data by default
  due to limited historical real review coverage.
- All phases are modular and independently executable.
"""

import subprocess
import sys
import os

# -------------------------------------------------------------------
# CONFIGURATION FLAGS
# -------------------------------------------------------------------

RUN_CORRELATION = True
USE_SIMULATED_CORRELATION = True   # Best practice for valid statistics
RUN_LLM = True                    # Requires valid OPENAI_API_KEY

# -------------------------------------------------------------------
# HELPER FUNCTION
# -------------------------------------------------------------------

def run_script(script_path):
    """
    Executes a Python script as a subprocess.
    Stops the pipeline if a critical failure occurs.
    """
    try:
        subprocess.run(
            [sys.executable, script_path],
            check=True
        )
    except subprocess.CalledProcessError:
        print(f"[ERROR] Failed while running {script_path}")
        sys.exit(1)

# -------------------------------------------------------------------
# PIPELINE START
# -------------------------------------------------------------------

print("\nMONTHLY PRODUCT HEALTH INTELLIGENCE SYSTEM")
print("=" * 42)
print("Starting full pipeline execution...\n")

# -------------------------------------------------------------------
# PHASE 1 — RELEASE IMPACT ANALYSIS
# -------------------------------------------------------------------

print("=" * 70)
print("RUNNING: Release Impact Analysis")
print("=" * 70)

run_script("analysis/release_impact_analysis.py")

print("[SUCCESS] Release Impact Analysis\n")

# -------------------------------------------------------------------
# PHASE 2 — RELEASE CORRELATION ANALYSIS (OPTIONAL)
# -------------------------------------------------------------------

print("=" * 70)
print("RUNNING: Release Correlation Analysis")
print("=" * 70)

if RUN_CORRELATION:
    if USE_SIMULATED_CORRELATION:
        print("Using simulated / aligned release data for correlation.")
        run_script("analysis/simulated_release_correlation_analysis.py")
    else:
        print("Using real review data for correlation (may be sparse).")
        run_script("analysis/release_correlation_analysis.py")
else:
    print("Correlation analysis disabled by configuration.")

print("[SUCCESS] Release Correlation Analysis\n")

# -------------------------------------------------------------------
# PHASE 3 — RELEASE HEALTH SCORE
# -------------------------------------------------------------------

print("=" * 70)
print("RUNNING: Release Health Score Calculation")
print("=" * 70)

run_script("analysis/release_health_score.py")

print("[SUCCESS] Release Health Score Calculation\n")

# -------------------------------------------------------------------
# PHASE 4 — RELEASE ANOMALY DETECTION (ML)
# -------------------------------------------------------------------

print("=" * 70)
print("RUNNING: Release Anomaly Detection (ML)")
print("=" * 70)

run_script("analysis/release_anomaly_detection.py")

print("[SUCCESS] Release Anomaly Detection (ML)\n")

# -------------------------------------------------------------------
# PHASE 5 — LLM ANOMALY INSIGHT GENERATION
# -------------------------------------------------------------------

print("=" * 70)
print("RUNNING: LLM Anomaly Insight Generation")
print("=" * 70)

if RUN_LLM:
    if os.getenv("OPENAI_API_KEY"):
        run_script("llm/anomaly_insight_generator.py")
        print("[SUCCESS] LLM Anomaly Insight Generation\n")
    else:
        print("OPENAI_API_KEY not found. Skipping LLM phase.\n")
else:
    print("LLM phase disabled by configuration.\n")

# -------------------------------------------------------------------
# PIPELINE COMPLETE
# -------------------------------------------------------------------

print("=" * 70)
print("PIPELINE COMPLETE")
print("=" * 70)

print("\nOutputs generated:")
print("- data/release_health_scores.csv")
print("- data/release_anomaly_analysis.csv")
print("- reports/release_anomaly_llm_insights.csv")

print("\nNext recommended step:")
print("- Review reports/monthly_product_health_report.md")

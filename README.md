Monthly Product Health Intelligence System

Overview
The Monthly Product Health Intelligence System is an end-to-end internal analytics pipeline designed to monitor product health across releases using real and simulated data, machine learning, and LLM-based explanations.

This project mirrors how product analytics and data science teams operate inside SaaS companies, focusing on data pipelines, analytics logic, anomaly detection, and explainability.

Problem Statement
Product teams need to understand:
- Whether a release negatively impacted users
- Whether support tickets increased after a release
- Whether review ratings declined
- Which releases are risky and require investigation
- How insights can be communicated clearly to stakeholders

System Architecture

Data Sources
    |
    v
Ingestion Layer (Python)
    |
    v
MongoDB (product_analytics)
    |
    v
ETL & Feature Engineering
    |
    v
Analytics & Health Scoring
    |
    v
ML Anomaly Detection (Isolation Forest)
    |
    v
LLM Insight Generation
    |
    v
Monthly Product Health Report

Project Structure
- ingestion: Load raw data into MongoDB
- scraping: External data collection and simulation
- etl: Data cleaning and normalization
- analysis: Analytics, scoring, and ML
- llm: LLM-based explanations
- data: Intermediate and final datasets
- reports: Final stakeholder outputs

Analytics and Modeling
Release Impact Analysis compares metrics before and after releases.
Health Scores are rule-based for transparency.
Correlation Analysis uses simulated data when real coverage is limited.
Anomaly Detection uses Isolation Forest.
LLM generates human-readable explanations only.

How to Run
python analysis/monthly_product_health_intelligence.py

Outputs
- release_health_scores.csv
- release_anomaly_analysis.csv
- release_anomaly_llm_insights.csv
- monthly_product_health_report.md

Summary
Built an internal monthly product analytics pipeline that ingests multiple data sources, stores them in MongoDB, performs ETL, analyzes release impact, detects anomalies using ML, and explains insights using LLMs.
# Monthly Product Health Intelligence System

An end-to-end product analytics system designed to evaluate release health, detect anomalies, and provide actionable insights using data engineering, machine learning, and business intelligence.

## Problem Statement

Product releases often impact customer experience, support load, and overall system stability. This project analyzes multiple product signals to identify risky releases and monitor product health over time.

## Tech Stack

* Python (Pandas, NumPy)
* Machine Learning (Isolation Forest)
* MongoDB (NoSQL Database)
* Power BI (Dashboard & Visualization)
* LLM-based Insights (AI explanations)

## Key Features

* Product health score calculation based on multiple metrics
* Anomaly detection using Isolation Forest
* Risk classification (Low, Medium, High)
* Correlation analysis using simulated data
* AI-based anomaly explanations
* Interactive Power BI dashboard for business insights

## Pipeline Flow

1. Data Ingestion (product releases, reviews, support tickets, usage data)
2. Data Cleaning and Feature Engineering
3. Product Health Score Calculation
4. Anomaly Detection using Machine Learning
5. AI-based Insight Generation (LLM)
6. Dashboard Visualization using Power BI

## Datasets Used

* Product release data
* Customer review data
* Support ticket data
* Product usage metrics
* Simulated data for correlation analysis


## Dashboard

Power BI dashboard for product health and anomaly analysis.

<img width="1306" height="737" alt="image" src="https://github.com/user-attachments/assets/2cd50dcd-5c72-4cf7-8740-4c30492914e0" />



## Project Structure

analysis/ → Core analytics and ML logic
ingestion/ → Data loading and preprocessing scripts
llm/ → AI-based anomaly explanation generation
reports/ → Generated reports and insights

## Sample Insights

* Identification of high-risk releases based on ticket spikes and rating drops
* Detection of anomalous releases using Isolation Forest
* Clear visualization of product health trends over time

## Key Learnings

* Built an end-to-end data pipeline
* Applied machine learning for anomaly detection
* Integrated structured and unstructured data
* Developed business-ready dashboards for decision-making


## Outcome

Enabled early detection of risky product releases and supported data-driven decision-making for product and engineering teams.

## Future Improvements

* Real-time data pipeline integration
* Advanced anomaly detection models
* Automated alert system for high-risk releases
* Deployment using cloud platforms

Project created & developed by:- Anand Kishore

# Customer Retention Intelligence System

A machine learning–driven customer churn prediction and retention analytics platform designed to help subscription businesses identify at-risk customers and take proactive action.

## 🚀 Overview
This project builds a complete end-to-end churn intelligence system using real telecom customer data. It combines exploratory data analysis, statistical insights, and machine learning to predict customer churn and quantify revenue at risk.

## 📊 Dataset
IBM Telco Customer Churn Dataset (7,000+ customers)

Features include:
- Tenure
- Monthly & Total Charges
- Contract Type
- Internet Service
- Payment Method
- Customer Demographics

Target:
- Churn (Yes / No)

## 🔍 Key Insights
- Month-to-month customers churn 15× more than two-year contract users
- Fiber optic users show the highest churn
- High-paying customers are more likely to leave

## 🤖 Machine Learning
Model: Logistic Regression  
Metrics:
- ROC AUC ≈ 0.80+

The model predicts churn probability for each customer and identifies the strongest churn drivers.

## 🧠 Churn Intelligence Engine
The system generates:
- Individual churn risk scores
- High-risk customer lists
- Revenue at risk estimates

This enables targeted retention strategies such as discounts, service improvements, and contract upgrades.

<img width="614" height="924" alt="image" src="https://github.com/user-attachments/assets/fd777dec-d4f9-40fb-b128-3fd1893a7e36" />

## 📁 Project Structure
```
Customer-Retention-Intelligence-System/
├── data/
├── notebooks/
├── models/
├── reports/
└── README.md
```
## 🛠 Tech Stack
- Python
- Pandas, NumPy
- Scikit-learn
- Matplotlib

## 📌 Use Case
Designed for subscription-based businesses such as telecom, SaaS, streaming, and e-commerce platforms to improve customer retention and reduce revenue loss.

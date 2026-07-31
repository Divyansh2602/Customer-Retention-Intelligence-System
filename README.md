# Customer Retention Intelligence System

**Predict who's about to churn, quantify what it costs, and act before they leave.**

An end-to-end churn-analytics project on 7,043 telecom customers: a machine-learning
model scores every customer's likelihood of leaving, and an interactive **Power BI**
dashboard turns those scores into a prioritized, money-aware retention plan.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi&logoColor=black)
![Dataset](https://img.shields.io/badge/customers-7%2C043-2E75B6)

![Churn analytics dashboard](dashboard/churn_dashboard.png)

---

## Why it matters

For any subscription business, keeping a customer is far cheaper than winning a new
one — but retention budgets are limited. This project answers three questions a
commercial team actually asks:

1. **Who is likely to churn?** — a probability score for every customer.
2. **How much is it worth?** — the revenue at risk behind each customer and segment.
3. **Where should we act first?** — the high-value, high-risk segment to target.

## Results at a glance

| Metric | Value |
|---|---|
| Customers analysed | **7,043** |
| Overall churn rate | **26.5%** |
| Annual **revenue at risk** | **~$1.68M** |
| High-risk customers flagged | **1,567** |
| Churn model — ROC AUC | **0.84** |

## Key insights

- **Contract type is the #1 driver.** Month-to-month customers churn ~**15×** more
  than two-year contract holders (≈43% vs ≈3%) — and they carry the bulk of the
  revenue at risk.
- **The first year is the danger zone.** Churn peaks in the 0–12 month tenure band
  and falls steadily as customers mature.
- **Fiber-optic and electronic-check customers churn most** — clear, targetable
  operational signals.
- **Revenue at risk concentrates** in month-to-month, short-tenure customers — the
  exact segment a retention budget should hit first.

## How it works

```
data/WA_Fn-UseC_-Telco-Customer-Churn.csv     raw data (7,043 customers)
            |
scripts/build_dashboard.py                     clean -> train churn model ->
            |                                  score every customer ->
            |                                  derive risk tier + revenue-at-risk
            v
data/churn_scored.csv                          Power BI-ready table (one row / customer)
dashboard/churn_dashboard.png                  rendered dashboard preview
```

- **Churn model** — Logistic Regression (standardized features), **ROC AUC ≈ 0.84**,
  producing a churn probability for every customer.
- **Risk tier** — High (p ≥ 0.50) · Medium (0.30–0.50) · Low (< 0.30).
- **Revenue at risk** — `MonthlyCharges × 12 × churn_probability`: the expected annual
  revenue lost from a customer, weighted by how likely they are to leave.

## The Power BI dashboard

The interactive dashboard is built in **Power BI Desktop** (free) from
`data/churn_scored.csv`: KPI cards, churn-rate breakdowns by contract / tenure /
payment method, a risk-tier split, and revenue-at-risk views — all cross-filtered by
slicers.

- **Build guide:** [`powerbi/BUILD_GUIDE.md`](powerbi/BUILD_GUIDE.md) — step by step, ~45 min.
- **DAX measures:** [`powerbi/DAX_measures.md`](powerbi/DAX_measures.md) — copy-paste ready.

## Reproduce

```bash
pip install -r requirements.txt
python scripts/build_dashboard.py
```

Regenerates `data/churn_scored.csv` and the dashboard preview, and prints the KPIs
and model AUC.

## Project structure

```
Customer-Retention-Intelligence-System/
├── data/
│   ├── WA_Fn-UseC_-Telco-Customer-Churn.csv   raw dataset
│   └── churn_scored.csv                        scored, Power BI-ready output
├── scripts/
│   └── build_dashboard.py                      data pipeline + model + preview
├── notebooks/
│   └── Customer_Retention_Intelligence_System.ipynb   exploratory analysis
├── models/
│   └── churn_model.pkl                         trained model
├── powerbi/
│   ├── BUILD_GUIDE.md                          how to build the dashboard
│   └── DAX_measures.md                         DAX for every measure
├── dashboard/
│   └── churn_dashboard.png                     rendered preview
└── requirements.txt
```

## Tech stack

**Python** (pandas, NumPy, scikit-learn, matplotlib) for the data pipeline and model ·
**Power BI + DAX** for the interactive dashboard.

## Dataset

[IBM Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
— 7,043 customers with contract, tenure, charges, services, demographics, and a churn
label.

## Use case

Built for subscription businesses — telecom, SaaS, streaming, e-commerce — to identify
at-risk customers, quantify revenue exposure, and target retention (discounts, service
fixes, contract upgrades) where it pays off most.

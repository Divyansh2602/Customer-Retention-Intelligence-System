"""
Customer Churn Analytics — data pipeline for the Power BI dashboard.

Takes the raw Telco churn data, trains a churn-probability model, and produces:
  1. data/churn_scored.csv  — a Power BI-ready table with, per customer:
        churn_probability, risk_tier (High/Medium/Low), revenue_at_risk, tenure_bucket
  2. dashboard/churn_dashboard.png — a rendered preview of the target dashboard
It also prints the headline KPIs and the model's ROC AUC.

Run:  python scripts/build_dashboard.py
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_auc_score

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Find the raw Telco dataset, whatever it's named in this repo.
def _find_raw():
    candidates = ["telco_churn.csv", "WA_Fn-UseC_-Telco-Customer-Churn.csv"]
    for name in candidates:
        p = os.path.join(HERE, "data", name)
        if os.path.exists(p):
            return p
    raise FileNotFoundError("No Telco churn CSV found in data/ (looked for: %s)" % candidates)

RAW  = _find_raw()
OUT  = os.path.join(HERE, "data", "churn_scored.csv")
PNG  = os.path.join(HERE, "dashboard", "churn_dashboard.png")
os.makedirs(os.path.join(HERE, "dashboard"), exist_ok=True)

# ── 1. Load & clean ──────────────────────────────────────────────────────────
df = pd.read_csv(RAW)
# TotalCharges has blank strings for brand-new (tenure 0) customers.
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0.0)
df["churn_flag"] = (df["Churn"] == "Yes").astype(int)

# ── 2. Train a churn-probability model ───────────────────────────────────────
target = "churn_flag"
drop_cols = ["customerID", "Churn", "churn_flag"]
X = pd.get_dummies(df.drop(columns=drop_cols), drop_first=True)
y = df[target]

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
model.fit(X_tr, y_tr)
auc = roc_auc_score(y_te, model.predict_proba(X_te)[:, 1])

# Score every customer for the dashboard.
df["churn_probability"] = model.predict_proba(X)[:, 1].round(4)

# ── 3. Business columns ──────────────────────────────────────────────────────
def tier(p):
    return "High" if p >= 0.50 else ("Medium" if p >= 0.30 else "Low")
df["risk_tier"] = df["churn_probability"].apply(tier)

# Expected annual revenue lost = monthly bill x 12 x probability of leaving.
df["revenue_at_risk"] = (df["MonthlyCharges"] * 12 * df["churn_probability"]).round(2)

bins   = [-1, 12, 24, 48, np.inf]
labels = ["0-12", "13-24", "25-48", "49+"]
df["tenure_bucket"] = pd.cut(df["tenure"], bins=bins, labels=labels)

keep = ["customerID", "gender", "SeniorCitizen", "Partner", "Dependents", "tenure",
        "tenure_bucket", "Contract", "InternetService", "PaymentMethod",
        "MonthlyCharges", "TotalCharges", "Churn", "churn_probability",
        "risk_tier", "revenue_at_risk"]
df[keep].to_csv(OUT, index=False)

# ── 4. Headline KPIs ─────────────────────────────────────────────────────────
total          = len(df)
churn_rate     = df["churn_flag"].mean()
rev_at_risk    = df["revenue_at_risk"].sum()
high_risk      = (df["risk_tier"] == "High").sum()
print(f"customers            : {total:,}")
print(f"churn rate           : {churn_rate:.1%}")
print(f"revenue at risk (yr) : ${rev_at_risk:,.0f}")
print(f"high-risk customers  : {high_risk:,}")
print(f"model ROC AUC        : {auc:.3f}")

# ── 5. Render a dashboard preview ────────────────────────────────────────────
BLUE, RED, GREY = "#2E75B6", "#C0392B", "#7F8C8D"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": "#DDDDDD",
                     "axes.grid": True, "grid.color": "#EEEEEE", "axes.axisbelow": True})
fig = plt.figure(figsize=(15, 8.2))
fig.suptitle("Customer Churn & Retention — Analytics Dashboard", fontsize=17, fontweight="bold", x=0.5, y=0.98)
gs = GridSpec(3, 4, figure=fig, hspace=0.55, wspace=0.32,
              left=0.05, right=0.97, top=0.90, bottom=0.06)

# KPI cards
kpis = [("Customers", f"{total:,}", BLUE),
        ("Churn Rate", f"{churn_rate:.1%}", RED),
        ("Revenue at Risk / yr", f"${rev_at_risk/1e6:.2f}M", RED),
        ("High-Risk Customers", f"{high_risk:,}", "#E67E22")]
for i, (label, val, col) in enumerate(kpis):
    ax = fig.add_subplot(gs[0, i]); ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, facecolor="#F7F9FC", edgecolor="#E1E6EF"))
    ax.text(0.5, 0.62, val, ha="center", va="center", fontsize=22, fontweight="bold", color=col, transform=ax.transAxes)
    ax.text(0.5, 0.24, label, ha="center", va="center", fontsize=10.5, color="#555", transform=ax.transAxes)

def churn_rate_by(col):
    return df.groupby(col)["churn_flag"].mean().sort_values(ascending=False)

# Churn rate by contract
ax = fig.add_subplot(gs[1, 0])
s = churn_rate_by("Contract")
ax.bar(range(len(s)), s.values * 100, color=BLUE)
ax.set_xticks(range(len(s))); ax.set_xticklabels(s.index, rotation=20, ha="right", fontsize=8.5)
ax.set_title("Churn rate by contract", fontweight="bold"); ax.set_ylabel("%")

# Churn rate by tenure bucket
ax = fig.add_subplot(gs[1, 1])
s = df.groupby("tenure_bucket", observed=True)["churn_flag"].mean().reindex(labels)
ax.bar(range(len(s)), s.values * 100, color=BLUE)
ax.set_xticks(range(len(s))); ax.set_xticklabels(s.index, fontsize=8.5)
ax.set_title("Churn rate by tenure (months)", fontweight="bold"); ax.set_ylabel("%")

# Churn rate by payment method
ax = fig.add_subplot(gs[1, 2])
s = churn_rate_by("PaymentMethod")
ax.barh(range(len(s)), s.values * 100, color=GREY)
ax.set_yticks(range(len(s))); ax.set_yticklabels([x.replace(" (automatic)", "") for x in s.index], fontsize=7.5)
ax.set_title("Churn rate by payment method", fontweight="bold"); ax.set_xlabel("%")

# Risk-tier distribution
ax = fig.add_subplot(gs[1, 3])
order = ["High", "Medium", "Low"]
s = df["risk_tier"].value_counts().reindex(order)
ax.bar(range(3), s.values, color=[RED, "#E67E22", "#27AE60"])
ax.set_xticks(range(3)); ax.set_xticklabels(order, fontsize=9)
ax.set_title("Customers by risk tier", fontweight="bold"); ax.set_ylabel("count")

# Revenue at risk by contract
ax = fig.add_subplot(gs[2, 0:2])
s = df.groupby("Contract")["revenue_at_risk"].sum().sort_values(ascending=False)
ax.bar(range(len(s)), s.values / 1e6, color=RED)
ax.set_xticks(range(len(s))); ax.set_xticklabels(s.index, fontsize=9)
ax.set_title("Revenue at risk by contract ($M / yr)", fontweight="bold"); ax.set_ylabel("$M")

# Revenue at risk by tenure bucket
ax = fig.add_subplot(gs[2, 2:4])
s = df.groupby("tenure_bucket", observed=True)["revenue_at_risk"].sum().reindex(labels)
ax.bar(range(len(s)), s.values / 1e6, color=RED)
ax.set_xticks(range(len(s))); ax.set_xticklabels(s.index, fontsize=9)
ax.set_title("Revenue at risk by tenure ($M / yr)", fontweight="bold"); ax.set_ylabel("$M")

fig.text(0.05, 0.015, f"Source: Telco churn dataset (7,043 customers)  |  Churn model ROC AUC = {auc:.2f}  |  "
                      "Revenue at risk = MonthlyCharges x 12 x churn probability",
         fontsize=8, color="#888")
fig.savefig(PNG, dpi=130, bbox_inches="tight", facecolor="white")
print(f"\nwrote {OUT}")
print(f"wrote {PNG}")

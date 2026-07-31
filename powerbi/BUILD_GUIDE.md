# Building the Dashboard in Power BI Desktop

Time: ~45–60 minutes. Power BI Desktop is free from the Microsoft Store.
The target layout is `dashboard/churn_dashboard.png`.

## 1. Load the data
1. **Home → Get data → Text/CSV** → select `data/churn_scored.csv` → **Load**.
2. In **Table view**, confirm data types:
   - `churn_probability`, `revenue_at_risk`, `MonthlyCharges`, `TotalCharges` → **Decimal number**
   - `tenure`, `SeniorCitizen` → **Whole number**
   - everything else → **Text**.

## 2. Create the measures
Modeling → **New measure**, and paste each measure from
[DAX_measures.md](DAX_measures.md). Set the formats noted there
(Churn Rate → %, Total Revenue at Risk → currency).

## 3. Build the visuals

**Top row — 4 KPI cards** (visual: **Card**)
| Card | Field |
|---|---|
| Customers | `[Total Customers]` |
| Churn Rate | `[Churn Rate]` |
| Revenue at Risk / yr | `[Total Revenue at Risk]` |
| High-Risk Customers | `[High-Risk Customers]` |

**Middle row — churn drivers**
1. **Churn rate by contract** — Clustered column chart. Axis: `Contract`; Values: `[Churn Rate]`.
2. **Churn rate by tenure** — Clustered column. Axis: `tenure_bucket` (sort 0-12 → 49+); Values: `[Churn Rate]`.
3. **Churn rate by payment method** — Clustered bar. Axis: `PaymentMethod`; Values: `[Churn Rate]`.
4. **Customers by risk tier** — Clustered column. Axis: `risk_tier`; Values: `[Total Customers]`.

**Bottom row — the money view**
1. **Revenue at risk by contract** — Clustered column. Axis: `Contract`; Values: `[Total Revenue at Risk]`.
2. **Revenue at risk by tenure** — Clustered column. Axis: `tenure_bucket`; Values: `[Total Revenue at Risk]`.

## 4. Make it interactive
Add **Slicers** (top or side) for `Contract`, `risk_tier`, and `InternetService`.
Clicking any slicer or bar now cross-filters the whole page — that interactivity
is the point of Power BI.

## 5. Polish & export
- Give the page a title text box: *"Customer Churn & Retention — Analytics Dashboard"*.
- Use a consistent colour theme (View → Themes); red for churn/risk, blue for volume.
- **File → Save as** `powerbi/churn_dashboard.pbix`, and **File → Export → PDF**
  (or a screenshot) into this folder so the finished dashboard is viewable
  without Power BI.

## Tips
- Sort the tenure axis: select the visual → **… → Sort axis → tenure_bucket → Ascending**
  (or create a numeric sort column).
- To show churn rate as %, ensure the `[Churn Rate]` measure is formatted as
  Percentage — Power BI carries that format into every visual.

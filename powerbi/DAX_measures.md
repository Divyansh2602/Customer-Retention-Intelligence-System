# DAX Measures

Create these in Power BI (Modeling → New measure) after loading
`data/churn_scored.csv` as the table **`churn_scored`**. Paste each block as a
separate measure.

```DAX
Total Customers = DISTINCTCOUNT ( churn_scored[customerID] )
```

```DAX
Churned Customers =
CALCULATE ( [Total Customers], churn_scored[Churn] = "Yes" )
```

```DAX
Churn Rate =
DIVIDE ( [Churned Customers], [Total Customers] )
```
> Format this measure as **Percentage**.

```DAX
Total Revenue at Risk = SUM ( churn_scored[revenue_at_risk] )
```
> Format as **Currency**.

```DAX
High-Risk Customers =
CALCULATE ( [Total Customers], churn_scored[risk_tier] = "High" )
```

```DAX
Avg Churn Probability = AVERAGE ( churn_scored[churn_probability] )
```

```DAX
Avg Tenure (months) = AVERAGE ( churn_scored[tenure] )
```

```DAX
Avg Monthly Charges = AVERAGE ( churn_scored[MonthlyCharges] )
```

```DAX
Revenue at Risk % =
DIVIDE (
    [Total Revenue at Risk],
    SUMX ( churn_scored, churn_scored[MonthlyCharges] * 12 )
)
```
> Share of total annual revenue that is at risk. Format as **Percentage**.

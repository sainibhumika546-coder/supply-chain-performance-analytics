

---

 ## 📌 Project Overview

 This project is an **end-to-end Supply Chain Performance & Operations Analytics Control Tower** built to demonstrate how modern BI and analytics techniques can transform fragmented operational data into actionable business insights.

 The solution integrates **10 relational tables and 24,000+ transactions** across a 24-month period covering:

 - Procurement & supplier performance
- Manufacturing & quality
- Multi-echelon inventory
- Logistics & carrier reliability
- Commercial sales & profitability

 The analytical stack combines **Power BI, DAX, SQL, Python, and Power Query** to create an executive-ready analytics solution.

 > **Dataset:** Synthetic consumer electronics supply-chain data created for educational and portfolio purposes.

---

 ## 🎯 Business Objectives

 The project answers four core supply-chain questions:

 | Business Area | Key Question |
| --- | --- |
| 🏭 Procurement | Where are supplier concentration and lead-time risks? |
| 📦 Inventory | Where is working capital tied up, and where are stockout risks emerging? |
| 🚚 Logistics | Which carriers and delay causes are affecting fulfillment performance? |
| 💰 Commercial | How do discounts, products, and channels affect profitability? |

---

 # 📊 Executive KPI Snapshot

 | KPI | Result | Target / Benchmark |
| --- | --- | --- |
| 💰 Net Revenue | **$176.95M** | $165.00M |
| 📈 Operating Profit | **$48.56M** | $41.25M |
| 🏷️ Discounts Conceded | **$9.92M** | \< $8.00M |
| 🏭 Procurement Spend | **$78.13M** | — |
| ⏱️ Avg. Supplier Lead Time | **11.53 days** | 10.00 days |
| ✅ Quality Compliance | **96.63 / 100** | ≥ 95.00 |
| 🏭 Manufacturing Defect Rate | **0.629%** | \< 1.00% |
| 📦 Inventory Valuation | **$108.77M** | — |
| ⚠️ Overstocked Capital | **$15.69M** | \< $5.00M |
| 🚚 Freight Spend | **$19.42M** | — |
| 🚨 Delay Exception Rate | **7.64%** | \< 5.00% |
| 📦 OTIF | **92.36%** | 95.00% |

---

 # 🏗️ Data Architecture

 The project uses a **multi-fact star schema** with shared/conformed dimensions.

```
erDiagram
    dim_date ||--o{ fact_sales : date_key
    dim_date ||--o{ fact_production : date_key
    dim_date ||--o{ fact_inventory : date_key
    dim_date ||--o{ fact_procurement : order_date_key
    dim_date ||--o{ fact_shipment : ship_date_key

    dim_product ||--o{ fact_sales : product_id
    dim_product ||--o{ fact_procurement : product_id
    dim_product ||--o{ fact_production : product_id
    dim_product ||--o{ fact_inventory : product_id
    dim_product ||--o{ fact_shipment : product_id

    dim_customer ||--o{ fact_sales : customer_id
    dim_customer ||--o{ fact_shipment : customer_id

    dim_supplier ||--o{ fact_procurement : supplier_id

    dim_facility ||--o{ fact_production : facility_id
    dim_facility ||--o{ fact_inventory : facility_id
```

 ## Dataset Structure

 | Table | Type | Rows | Purpose |
| --- | --- | --- | --- |
| `dim_date` | Dimension | 731 | Calendar & time intelligence |
| `dim_product` | Dimension | 16 | Product catalog & standard costs |
| `dim_customer` | Dimension | 5 | Customer/channel master |
| `dim_supplier` | Dimension | 7 | Supplier master |
| `dim_facility` | Dimension | 6 | Plant & DC master |
| `fact_procurement` | Fact | 2,200 | Purchase orders & supplier performance |
| `fact_production` | Fact | 4,500 | Production batches & defects |
| `fact_inventory` | Fact | 1,152 | Inventory positions & safety stock |
| `fact_shipment` | Fact | 7,500 | Outbound logistics & SLA performance |
| `fact_sales` | Fact | 8,500 | Revenue, discounts & profitability |

---

 # 🔧 Data Modeling & Engineering

 Several modeling and calculation issues were identified and corrected during the data audit.

 ### 1\. Inventory Capital Valuation

 Instead of treating inventory units as monetary value:

```
SUM(fact_inventory[stock_level])
```

 the model calculates inventory capital using product-level standard cost:

```
Inventory Valuation =
SUMX(
    fact_inventory,
    fact_inventory[stock_level]
        * RELATED(dim_product[unit_cost])
)
```

 **Result:** `$108.77M` inventory valuation.

---

 ### 2\. COGS vs Procurement Spend

 Sales cost and procurement expenditure were separated into independent measures.

 - **COGS:** `$128.39M`
- **Procurement Spend:** `$78.13M`

 This prevents procurement purchasing activity from being incorrectly treated as sales COGS.

---

 ### 3\. Time Intelligence

 Active date relationships were established between:

```
dim_date → fact_procurement
dim_date → fact_shipment
```

 This enables monthly and yearly analysis of procurement and logistics KPIs.

---

 ### 4\. Referential Integrity

 Orphan shipment foreign keys were identified and cleaned to prevent unexpected `(Blank)` categories in Power BI visuals.

---

 # 🖥️ Power BI Dashboard

 The dashboard contains **6 analytical pages**, designed around an executive control-tower workflow.

---

 ## 01 — Executive Operations Control Tower

 Provides an executive overview of:

 - Revenue & profitability
- Procurement spend
- Inventory valuation
- Supplier lead times
- Logistics delays
- Monthly financial trends
- Channel performance
- Product category contribution

---

 ## 02 — Procurement & Supplier Risk

 Analyzes:

 - Supplier spend concentration
- Lead-time performance
- Quality scores
- Sourcing geography
- Purchase price variance
- Supplier risk exposure

 Example analysis:

 > Top 3 suppliers represent **43.8% of procurement spend**.

---

 ## 03 — Inventory & Operations Health

 Tracks:

 - Inventory capital allocation
- Safety-stock coverage
- Reorder points
- Overstock positions
- Stockout risks
- Manufacturing defect rates
- Facility performance

 Key finding:

 > **$15.69M** of inventory capital is classified as overstocked.

---

 ## 04 — Logistics & Carrier Reliability

 Analyzes:

 - Carrier delay rates
- Freight expenditure
- Delay root causes
- Cost vs reliability
- Shipment SLA performance
- Carrier performance quadrants

 Overall logistics performance:

 **92.36% OTIF** with a **7.64% delay exception rate**.

---

 ## 05 — Commercial Sales & Profitability

 Analyzes:

 - Revenue by SKU
- Product profitability
- Customer/account contribution
- Discount erosion
- Net margin
- Pareto revenue concentration

 The dashboard uses an **80/20 Pareto analysis** to identify products responsible for the majority of revenue contribution.

---

 ## 06 — Strategic Insights & Action Matrix

 Converts analytical findings into structured management actions.

 The page connects:

```
Observation
     ↓
Business Impact
     ↓
Root Cause
     ↓
Recommended Action
     ↓
Expected Operational Outcome
```

---

 # 🔍 Key Business Findings

 ## 🏭 Procurement

 Supplier lead times vary significantly by sourcing geography.

 | Geography | Avg. Lead Time |
| --- | --- |
| China | 12.47 days |
| Japan | 12.42 days |
| Vietnam | 9.39 days |

The analysis also identifies elevated P95 lead-time requirements, which can influence safety-stock requirements.

---

 ## 📦 Inventory

 The model identifies two opposing inventory problems:

 - **$15.69M** in overstocked capital
- **25 DC inventory snapshots** classified as critical stockout risk

 This highlights the importance of balancing service-level requirements against working-capital efficiency.

---

 ## 🚚 Logistics

 The dataset contains:

 - **7,500 shipments**
- **$19.42M freight expenditure**
- **573 delayed shipments**
- **7.64% delay exception rate**

 Delay analysis categorizes exceptions into operational causes such as:

 - Carrier capacity
- Documentation
- Port congestion
- Other logistics exceptions

---

 ## 💰 Commercial

 Commercial discounts total:

 **$9.92M**

 The profitability analysis evaluates discount behavior against realized margins and identifies products and channels where discounting has a material effect on profitability.

---

 # 🧮 SQL Analytics

 The SQL layer contains **10+ analytical queries** using:

 - CTEs
- Window functions
- `SUM() OVER()`
- `LAG()`
- Ranking functions
- Conditional aggregation
- Pareto analysis
- Margin calculations

 ### Example — Product Pareto Analysis

```
WITH ProductSummary AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        SUM(s.quantity_sold) AS units_sold,
        SUM(s.net_revenue) AS total_revenue,
        SUM(s.profit) AS total_profit,
        ROUND(
            SUM(s.profit) /
            NULLIF(SUM(s.net_revenue), 0) * 100,
            2
        ) AS margin_pct
    FROM fact_sales s
    JOIN dim_product p
        ON s.product_id = p.product_id
    GROUP BY
        p.product_id,
        p.product_name,
        p.category
),

ParetoCalculations AS (
    SELECT
        *,
        SUM(total_revenue) OVER (
            ORDER BY total_revenue DESC
        ) AS cumulative_revenue,

        SUM(total_revenue) OVER () AS total_company_revenue

    FROM ProductSummary
)

SELECT
    product_name,
    category,
    units_sold,
    total_revenue,
    total_profit,
    margin_pct,

    ROUND(
        total_revenue /
        total_company_revenue * 100,
        2
    ) AS revenue_share_pct,

    ROUND(
        cumulative_revenue /
        total_company_revenue * 100,
        2
    ) AS cumulative_revenue_share_pct,

    CASE
        WHEN cumulative_revenue /
             total_company_revenue <= 0.80
            THEN 'Tier A'

        WHEN cumulative_revenue /
             total_company_revenue <= 0.95
            THEN 'Tier B'

        ELSE 'Tier C'
    END AS pareto_classification

FROM ParetoCalculations
ORDER BY total_revenue DESC;
```

 📁 Full SQL analysis: `sql/supply_chain_analysis.sql`

---

 # 🐍 Python Analytics

 Python is used for data validation, statistical analysis, and visualization generation.

 ### `eda_and_summary.py`

 Performs:

 - Dataset profiling
- Null-value analysis
- Duplicate detection
- Referential-integrity checks
- Table-level summaries
- Data-quality validation

 ### `advanced_analytics.py`

 Performs:

 - Lead-time variance analysis
- P95 buffer calculations
- Inventory health classification
- Delay Pareto analysis
- Carrier cost/reliability analysis
- Operational risk diagnostics

 ### `generate_visuals.py`

 Generates:

 - Executive charts
- Supply-chain visualizations
- KPI graphics
- Dashboard assets
- High-resolution analytical visuals

---

 # 📈 Analytical Techniques

 This project demonstrates practical application of:

 - Multi-fact star schema modeling
- Dimensional modeling
- Power Query transformations
- DAX measures
- Time intelligence
- `SUMX` and `RELATED`
- Defensive division with `DIVIDE`
- Window functions
- CTE-based SQL analytics
- Pareto analysis
- Statistical distribution analysis
- P95 lead-time analysis
- Inventory segmentation
- Carrier cost/reliability analysis
- KPI benchmarking
- Executive dashboard design

---

 # 💡 Strategic Action Areas

 Based on the analytical findings, the project identifies several potential operational initiatives:

 ### 1\. Supplier Risk Management

 - Diversify sourcing where concentration is high.
- Establish supplier-specific SLA monitoring.
- Incorporate lead-time variability into procurement planning.

 ### 2\. Inventory Optimization

 - Recalculate safety stock using service-level and lead-time variability.
- Rebalance inventory between distribution centers.
- Identify slow-moving inventory for liquidation or redistribution.

 ### 3\. Logistics Optimization

 - Monitor carrier performance against cost and SLA simultaneously.
- Analyze recurring delay root causes.
- Improve documentation and customs workflows.

 ### 4\. Commercial Margin Management

 - Monitor discount rates at SKU and channel level.
- Identify products with significant discount-related margin erosion.
- Introduce approval thresholds for high-value discounts.

---

 # 📂 Repository Structure

```
Supply-Chain-Performance-Analytics/
│
├── README.md
├── LICENSE
│
├── dashboard/
│   ├── Supply_Chain_Operations_Analytics.pbix
│   └── DAX_Measures_Dictionary.md
│
├── data/
│   ├── dim_customer.csv
│   ├── dim_date.csv
│   ├── dim_facility.csv
│   ├── dim_product.csv
│   ├── dim_supplier.csv
│   ├── fact_inventory.csv
│   ├── fact_procurement.csv
│   ├── fact_production.csv
│   ├── fact_sales.csv
│   └── fact_shipment.csv
│
├── sql/
│   └── supply_chain_analysis.sql
│
├── python/
│   ├── eda_and_summary.py
│   ├── advanced_analytics.py
│   └── generate_visuals.py
│
├── screenshots/
│   ├── 00_hero_dashboard.png
│   ├── 01_executive_control_tower.png
│   ├── 02_procurement_supplier_risk.png
│   ├── 03_inventory_operations_health.png
│   ├── 04_logistics_carrier_performance.png
│   ├── 05_commercial_sales_profitability.png
│   └── 06_executive_insights_matrix.png
│
└── documentation/
    ├── Project_Report.pdf
    └── Interview_Preparation_Guide.md
```

---

 # 🚀 Future Enhancements

 ### 🔮 Demand Forecasting

 Integrate forecasting models such as:

 - ARIMA
- Prophet
- Machine-learning demand forecasting

 Potential outputs:

 - SKU-level demand forecasts
- Safety-stock recommendations
- Forecast accuracy tracking
- Seasonal demand patterns

 ### 📡 Real-Time Logistics

 Future versions could integrate:

 - GPS/container tracking
- Port congestion APIs
- Carrier APIs
- Real-time shipment status
- Automated exception alerts

 ### 🤖 Predictive Supply Chain Risk

 Potential future models:

```
Supplier Risk Prediction
        ↓
Stockout Probability
        ↓
Shipment Delay Prediction
        ↓
Inventory Optimization
        ↓
Recommended Action
```

---

 # 💼 Portfolio / Resume Highlights

 This project demonstrates experience with:

 - **Power BI dashboard development**
- **DAX data modeling and measure engineering**
- **SQL analytical querying**
- **Python data analytics**
- **Supply-chain KPI design**
- **Star-schema architecture**
- **Data-quality auditing**
- **Executive storytelling**
- **Business-oriented analytics**

 ### Resume-ready achievements

 > **Built an end-to-end Supply Chain Analytics Control Tower in Power BI, integrating 10 relational tables and 24,000+ transactions to monitor procurement, inventory, logistics, manufacturing, and commercial performance.**

 > **Developed advanced DAX and SQL analytics for inventory valuation, supplier lead-time analysis, carrier reliability, profitability, and 80/20 revenue segmentation.**

 > **Identified $15.69M in overstocked inventory capital and analyzed 573 logistics delay exceptions to support supply-chain optimization initiatives.**

---

 # ⚠️ Limitations

 This is a **synthetic educational portfolio project**. The dataset does not represent actual operational, financial, or supply-chain data from Samsung Electronics or any other real organization.

 Future versions may incorporate:

 - Real-time data pipelines
- Predictive forecasting
- Machine-learning models
- IoT/telematics data
- Automated Power BI refresh educational and portfolio case study using synthetic consumer-electronics supply-chain data. It is intended to demonstrate data analytics, business intelligence, SQL, Python,
- Cloud data warehousing
- Supply-chain scenario simulation

---

 # 📜 Disclaimer

 > This project is an independently developed educational and portfolio case study using synthetic consumer-electronics supply-chain data. It is intended to demonstrate data analytics, business intelligence, SQL, Python, DAX, and supply-chain modeling capabilities. It does not represent actual operational or financial data of Samsung Electronics.

---

 ## ⭐ If You Find This Project Useful

 Feel free to explore the dashboard, SQL analysis, Python scripts, and documentation.

 **Built with:** Power BI · DAX · SQL · Python · Power Query · MySQL · Pandas · NumPy

---

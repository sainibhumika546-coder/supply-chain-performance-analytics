# 🎙️ Data Analyst & BI Developer Interview Preparation Guide

**Project:** Supply Chain Performance & Operations Analytics  
**Focus:** Executive Storytelling, Data Modeling, DAX, SQL, Python, and Root-Cause Diagnostics

---

### Q1. "Tell me about this project."
> **Answer:**  
> "This is an end-to-end Supply Chain & Operations Analytics project where I designed a centralized Business Intelligence Control Tower for a global consumer electronics supply chain. The project integrates transactional data across 10 relational tables—spanning suppliers, procurement purchase orders, manufacturing facilities, multi-echelon inventory snapshots, logistics shipments, and commercial sales channels.  
> Rather than simply building standard descriptive charts, I designed the analysis around a core business problem: identifying capital inefficiencies, supplier risks, and logistics delivery bottlenecks across the supply chain. I extracted and cleaned the datasets, modeled a star schema in Power BI with 20+ production DAX measures, executed complex analytical SQL queries using CTEs and window functions, and performed statistical diagnostic modeling in Python."

---

### Q2. "What was the core business problem you aimed to solve?"
> **Answer:**  
> "Global hardware supply chains often suffer from fragmented visibility between procurement lead times, manufacturing buffers, carrier reliability, and commercial profit margins.  
> Specifically, management faced four critical questions:
> 1. *Procurement Risk:* Where are we vulnerable to supplier concentration and lead time volatility?
> 2. *Inventory Health:* Are we tying up excess working capital in slow-moving stock while simultaneously risking stockouts on flagship products?
> 3. *Logistics Reliability:* Which carriers are causing freight delivery delays, and what are the operational root causes?
> 4. *Commercial Profitability:* How do promotional discounts impact realized net profit margins across retail channels?  
> My objective was to unify these disparate data streams into a single interactive decision-support control tower."

---

### Q3. "How did you clean the data and what data issues did you discover?"
> **Answer:**  
> "During the initial data audit, I identified three major data and modeling issues:
> - **Inconsistent Metric Logic in Legacy Formulas:** In the legacy data model, 'Inventory Value' was calculated as `SUM(stock_level)`, which meant physical unit counts were being reported as dollar valuations ($160K units labeled as dollars). I refactored this using `SUMX(fact_inventory, stock_level * RELATED(dim_product[unit_cost]))` to correctly calculate the true financial valuation of $108.77M.
> - **COGS vs. Procurement Spend:** The legacy model conflated sales COGS with procurement purchase order spend. I separated these by computing true COGS from sales transactions ($128.39M) and tracking procurement spend independently ($78.13M).
> - **Orphan Keys & Disconnected Dimensions:** I found that legacy procurement and shipment tables lacked active relationships to the date dimension, preventing time intelligence. Additionally, over 4,000 shipment rows had product and customer keys that were unlisted in the dimension tables, which caused 70% blank visual slices in legacy charts. I cleaned the referential joins and enforced referential integrity in Power Query."

---

### Q4. "Why did you use a Star Schema for the data model?"
> **Answer:**  
> "A Star Schema is the industry gold standard for Power BI and tabular models for several reasons:
> 1. **VertiPaq Engine Optimization:** Power BI's in-memory columnar engine performs best with single-direction one-to-many relationships between centralized conformed dimension tables (`dim_date`, `dim_product`, `dim_customer`, `dim_supplier`, `dim_facility`) and separate fact tables (`fact_procurement`, `fact_production`, `fact_inventory`, `fact_shipment`, `fact_sales`).
> 2. **Eliminating Ambiguity:** By avoiding snowflake nesting or many-to-many bidirectional filtering, the model prevents ambiguous filter contexts, circular dependencies, and unexpected calculation errors.
> 3. **High Performance & Usability:** Business users and analysts can easily drag attributes from conformed dimensions to slice across multiple fact tables simultaneously without query performance degradation."

---

### Q5. "What DAX measures did you create, and how did you ensure DAX quality?"
> **Answer:**  
> "I developed 20+ production-grade DAX measures organized into dedicated display folders.  
> Key DAX practices I followed:
> - **Defensive Division:** Used `DIVIDE(numerator, denominator, 0)` to handle nulls and division-by-zero safely without throwing runtime errors.
> - **Iterator Functions:** Used `SUMX` with `RELATED()` to compute row-by-row row-context valuations such as `Total Inventory Valuation = SUMX(fact_inventory, fact_inventory[stock_level] * RELATED(dim_product[unit_cost]))`.
> - **Explicit Measures & Measure Branching:** Built atomic base measures (e.g., `[Total Net Revenue]`, `[Cost of Goods Sold]`) and reused them in higher-level KPI measures like `[Operating Profit Margin %]` to maintain a single source of truth.
> - **Filter Context Manipulation:** Utilized `CALCULATE` with explicit boolean filter conditions to isolate stockout risk snapshots (`stock_level < safety_stock_level`) and logistics delay exceptions (`status = 'Delayed'`)."

---

### Q6. "Why Power BI for this solution?"
> **Answer:**  
> "Power BI provides the ideal combination of enterprise ETL (Power Query), high-performance in-memory tabular modeling (VertiPaq / DAX), and interactive storytelling.  
> It allowed me to:
> - Create an executive control tower layout that lets leadership transition from high-level KPIs down into specific operational modules (Procurement, Inventory, Logistics, Commercial).
> - Enable dynamic cross-filtering between product lines, facilities, carriers, and geographical sourcing regions.
> - Deliver a responsive, modern visual theme designed for corporate decision-makers."

---

### Q7. "What analytical SQL queries did you write?"
> **Answer:**  
> "I wrote 10+ analytical SQL queries using advanced SQL techniques:
> - **Common Table Expressions (CTEs):** Structured multi-step queries for monthly financial trends, vendor concentration, and carrier benchmarking.
> - **Window Functions (`SUM() OVER()`, `LAG()`):** Calculated Month-over-Month (MoM) revenue growth % and Pareto 80/20 cumulative revenue contribution curves for the product portfolio.
> - **Categorical Case Statements:** Built dynamic risk categorization rules, such as classifying inventory positions into 'Critical Stockout Risk', 'Reorder Required', 'Healthy Buffer', and 'Excess/Overstocked'.
> - **Benchmarking Quadrants:** Classified carriers into strategic quadrants (High Value, Premium, Budget Risk, Underperforming) by comparing carrier-specific delay rates and average freight costs against global dataset averages."

---

### Q8. "What did you use Python for?"
> **Answer:**  
> "I used Python (`pandas`, `numpy`, `matplotlib`, `seaborn`) to perform the deep exploratory data analysis and statistical validation:
> 1. **Data Integrity & FK Audit:** Automated checks for missing values, duplicate primary keys, and foreign key orphans across 24,000+ total rows.
> 2. **Lead Time Statistical Modeling:** Calculated lead time variances, standard deviations, and 95th percentile buffer thresholds to identify unstable suppliers.
> 3. **Delay Root-Cause Pareto Analysis:** Analyzed frequency, affected unit volume, and freight cost impact across 8 distinct logistics delay reasons.
> 4. **Asset & Screenshot Generation:** Programmatically generated publication-quality dashboard visualization mockups and executive reports."

---

### Q9. "What was your most important analytical finding?"
> **Answer:**  
> "My most significant finding was the **dual-sided inventory imbalance**:  
> Out of $108.77M in total inventory valuation across warehouse snapshots, **$15.69M (14.4%) was locked up in overstocked positions** (>2.5x safety stock) in slower-moving tablet and accessory categories, creating unnecessary holding and capital costs.  
> Simultaneously, **25 warehouse snapshots suffered from critical stockout vulnerabilities** (stock < safety stock) concentrated in high-demand flagship smartphones (Galaxy S24 Ultra and Galaxy Z Fold5), which generate 43.7% of company revenue.  
> By presenting this finding alongside vendor lead time data, I demonstrated how East Asian supplier lead time volatility was directly causing buffer instability downstream, and recommended an automated reorder trigger combined with inter-DC stock rebalancing."

---

### Q10. "What would you improve or build next if you had access to more data?"
> **Answer:**  
> "If additional data were available, I would expand the project in three key directions:
> 1. **Real-Time Telematics & Weather Data:** Integrate IoT GPS tracking and port weather API feeds into the logistics module to predict shipment delays before they occur.
> 2. **Machine Learning Demand Forecasting:** Build a time-series forecasting model (e.g., Prophet or XGBoost) to forecast SKU-level demand by region, allowing proactive reorder point adjustments.
> 3. **Supplier Cost Breakdown & Inflation Indices:** Incorporate raw material commodity price indices (semiconductor silicon, lithium, aluminum) to perform true purchase price variance (PPV) predictive modeling."

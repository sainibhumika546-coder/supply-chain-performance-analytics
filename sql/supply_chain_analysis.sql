/*
====================================================================================================
PROJECT: Supply Chain Performance & Operations Analytics
AUTHOR: Data Analytics Portfolio
DATABASE: ANSI SQL / MySQL 8.0+ / PostgreSQL / Snowflake Compatible
DESCRIPTION: Comprehensive End-to-End Supply Chain, Procurement, Logistics, and Commercial Analytics
====================================================================================================

SCHEMA OVERVIEW:
- Dimension Tables: dim_date, dim_product, dim_customer, dim_supplier, dim_facility
- Fact Tables: fact_procurement, fact_production, fact_inventory, fact_shipment, fact_sales

====================================================================================================
*/

-- =================================================================================================
-- 1. EXECUTIVE MONTHLY FINANCIAL & MARGIN TRAJECTORY
-- Purpose: Track monthly Gross Revenue, Net Revenue, COGS, Discounts, Net Profit, and MoM Margin %
-- =================================================================================================
WITH MonthlyFinancials AS (
    SELECT
        d.year,
        d.month,
        d.month_name,
        COUNT(DISTINCT s.sales_id) AS total_orders,
        SUM(s.quantity_sold) AS total_units_sold,
        SUM(s.gross_revenue) AS gross_revenue,
        SUM(s.discount_amount) AS total_discounts,
        SUM(s.net_revenue) AS net_revenue,
        SUM(s.total_cost) AS total_cogs,
        SUM(s.profit) AS net_profit,
        ROUND((SUM(s.profit) / NULLIF(SUM(s.net_revenue), 0)) * 100, 2) AS profit_margin_pct,
        ROUND((SUM(s.discount_amount) / NULLIF(SUM(s.gross_revenue), 0)) * 100, 2) AS discount_rate_pct
    FROM fact_sales s
    JOIN dim_date d ON s.date_key = d.date_key
    GROUP BY d.year, d.month, d.month_name
)
SELECT
    year,
    month,
    month_name,
    total_orders,
    total_units_sold,
    net_revenue,
    total_cogs,
    net_profit,
    profit_margin_pct,
    discount_rate_pct,
    -- Month-over-Month Revenue Growth %
    ROUND(
        ((net_revenue - LAG(net_revenue) OVER (ORDER BY year, month)) / 
        NULLIF(LAG(net_revenue) OVER (ORDER BY year, month), 0)) * 100, 2
    ) AS mom_revenue_growth_pct,
    -- Month-over-Month Profit Growth %
    ROUND(
        ((net_profit - LAG(net_profit) OVER (ORDER BY year, month)) / 
        NULLIF(LAG(net_profit) OVER (ORDER BY year, month), 0)) * 100, 2
    ) AS mom_profit_growth_pct
FROM MonthlyFinancials
ORDER BY year, month;


-- =================================================================================================
-- 2. PRODUCT PORTFOLIO PROFITABILITY & PARETO (80/20) REVENUE ANALYSIS
-- Purpose: Identify top revenue drivers and cumulative share to assess product concentration risk
-- =================================================================================================
WITH ProductSummary AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        p.product_line,
        SUM(s.quantity_sold) AS units_sold,
        SUM(s.net_revenue) AS total_revenue,
        SUM(s.profit) AS total_profit,
        ROUND((SUM(s.profit) / NULLIF(SUM(s.net_revenue), 0)) * 100, 2) AS margin_pct,
        SUM(s.discount_amount) AS total_discount_given
    FROM fact_sales s
    JOIN dim_product p ON s.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, p.category, p.product_line
),
ParetoCalculations AS (
    SELECT
        product_id,
        product_name,
        category,
        product_line,
        units_sold,
        total_revenue,
        total_profit,
        margin_pct,
        total_discount_given,
        -- Window function to calculate cumulative revenue
        SUM(total_revenue) OVER (ORDER BY total_revenue DESC) AS cumulative_revenue,
        SUM(total_revenue) OVER () AS total_company_revenue
    FROM ProductSummary
)
SELECT
    product_name,
    category,
    product_line,
    units_sold,
    total_revenue,
    total_profit,
    margin_pct,
    ROUND((total_revenue / total_company_revenue) * 100, 2) AS revenue_share_pct,
    ROUND((cumulative_revenue / total_company_revenue) * 100, 2) AS cumulative_revenue_share_pct,
    CASE 
        WHEN (cumulative_revenue / total_company_revenue) <= 0.80 THEN 'Tier A (Top 80% Contributor)'
        WHEN (cumulative_revenue / total_company_revenue) <= 0.95 THEN 'Tier B (Next 15% Contributor)'
        ELSE 'Tier C (Tail 5% Contributor)'
    END AS pareto_classification
FROM ParetoCalculations
ORDER BY total_revenue DESC;


-- =================================================================================================
-- 3. SUPPLIER CONCENTRATION RISK & LEAD TIME VARIABILITY
-- Purpose: Evaluate vendor spend share, delivery stability, and quality scores
-- =================================================================================================
WITH SupplierMetrics AS (
    SELECT
        sup.supplier_id,
        sup.supplier_name,
        sup.country,
        sup.tier,
        sup.specialty,
        COUNT(pr.procurement_id) AS total_purchase_orders,
        SUM(pr.order_quantity) AS total_units_procured,
        SUM(pr.total_cost) AS total_spend,
        AVG(pr.lead_time_days) AS avg_lead_time_days,
        MIN(pr.lead_time_days) AS min_lead_time_days,
        MAX(pr.lead_time_days) AS max_lead_time_days,
        AVG(pr.quality_score) AS avg_quality_score
    FROM fact_procurement pr
    JOIN dim_supplier sup ON pr.supplier_id = sup.supplier_id
    GROUP BY sup.supplier_id, sup.supplier_name, sup.country, sup.tier, sup.specialty
),
TotalSpendSummary AS (
    SELECT SUM(total_spend) AS global_procurement_spend FROM SupplierMetrics
)
SELECT
    sm.supplier_name,
    sm.country,
    sm.tier,
    sm.specialty,
    sm.total_purchase_orders,
    sm.total_units_procured,
    sm.total_spend,
    ROUND((sm.total_spend / ts.global_procurement_spend) * 100, 2) AS spend_share_pct,
    ROUND(sm.avg_lead_time_days, 1) AS avg_lead_time_days,
    (sm.max_lead_time_days - sm.min_lead_time_days) AS lead_time_spread_days,
    ROUND(sm.avg_quality_score, 2) AS avg_quality_score,
    -- Supplier Risk Rating
    CASE 
        WHEN sm.avg_quality_score < 95.0 OR (sm.max_lead_time_days - sm.min_lead_time_days) >= 8 THEN 'High Risk / Unstable'
        WHEN sm.avg_quality_score < 97.0 THEN 'Moderate Risk'
        ELSE 'Preferred / Low Risk'
    END AS supplier_risk_status
FROM SupplierMetrics sm
CROSS JOIN TotalSpendSummary ts
ORDER BY sm.total_spend DESC;


-- =================================================================================================
-- 4. PROCUREMENT UNIT COST VARIANCE VS STANDARD PRODUCT BENCHMARK
-- Purpose: Detect pricing discrepancies and inflationary cost variances across procurement POs
-- =================================================================================================
SELECT
    p.product_name,
    p.category,
    p.unit_cost AS catalog_standard_cost,
    ROUND(AVG(pr.unit_cost), 2) AS realized_avg_procurement_cost,
    ROUND(MIN(pr.unit_cost), 2) AS min_procurement_cost,
    ROUND(MAX(pr.unit_cost), 2) AS max_procurement_cost,
    ROUND((AVG(pr.unit_cost) - p.unit_cost), 2) AS cost_variance_usd,
    ROUND(((AVG(pr.unit_cost) - p.unit_cost) / NULLIF(p.unit_cost, 0)) * 100, 2) AS cost_variance_pct
FROM fact_procurement pr
JOIN dim_product p ON pr.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category, p.unit_cost
ORDER BY cost_variance_pct DESC;


-- =================================================================================================
-- 5. INVENTORY BUFFER HEALTH & STOCKOUT VULNERABILITY AUDIT
-- Purpose: Compare current stock levels against safety stock thresholds and reorder points
-- =================================================================================================
WITH InventoryHealth AS (
    SELECT
        inv.inventory_id,
        p.product_name,
        p.category,
        p.unit_cost,
        f.facility_name,
        f.city AS facility_city,
        f.country AS facility_country,
        inv.stock_level,
        inv.safety_stock_level,
        inv.reorder_point,
        (inv.stock_level * p.unit_cost) AS total_inventory_value,
        CASE
            WHEN inv.stock_level < inv.safety_stock_level THEN 'Critical Stockout Risk'
            WHEN inv.stock_level <= inv.reorder_point THEN 'Reorder Required'
            WHEN inv.stock_level > (inv.safety_stock_level * 2.5) THEN 'Excess / Overstocked'
            ELSE 'Healthy Buffer'
        END AS inventory_health_status
    FROM fact_inventory inv
    JOIN dim_product p ON inv.product_id = p.product_id
    JOIN dim_facility f ON inv.facility_id = f.facility_id
)
SELECT
    inventory_health_status,
    COUNT(inventory_id) AS snapshot_count,
    SUM(stock_level) AS total_units_in_stock,
    ROUND(SUM(total_inventory_value), 2) AS total_inventory_valuation_usd,
    ROUND(AVG(stock_level - reorder_point), 1) AS avg_cushion_above_reorder
FROM InventoryHealth
GROUP BY inventory_health_status
ORDER BY total_inventory_valuation_usd DESC;


-- =================================================================================================
-- 6. MANUFACTURING DEFECT RATE & SCRAP YIELD LOSS BY FACILITY
-- Purpose: Analyze production efficiency, volume throughput, and defect intensity by site
-- =================================================================================================
SELECT
    f.facility_name,
    f.country AS plant_country,
    f.specialization,
    f.annual_capacity,
    COUNT(pr.production_id) AS production_runs,
    SUM(pr.quantity_produced) AS total_units_produced,
    SUM(pr.defective_units) AS total_defective_units,
    ROUND((CAST(SUM(pr.defective_units) AS FLOAT) / NULLIF(SUM(pr.quantity_produced), 0)) * 100, 3) AS actual_defect_rate_pct,
    ROUND(AVG(pr.defect_rate_pct), 3) AS reported_avg_defect_pct,
    -- Capacity Utilization Rate
    ROUND((SUM(pr.quantity_produced) / NULLIF(f.annual_capacity * 2, 0)) * 100, 2) AS estimated_utilization_pct
FROM fact_production pr
JOIN dim_facility f ON pr.facility_id = f.facility_id
GROUP BY f.facility_id, f.facility_name, f.country, f.specialization, f.annual_capacity
ORDER BY actual_defect_rate_pct DESC;


-- =================================================================================================
-- 7. LOGISTICS CARRIER PERFORMANCE, ON-TIME RELIABILITY & FREIGHT SPEND
-- Purpose: Rank logistics carriers based on delay frequency, total shipments, and cost efficiency
-- =================================================================================================
SELECT
    carrier,
    COUNT(shipment_id) AS total_shipments,
    SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END) AS delivered_count,
    SUM(CASE WHEN status = 'Delayed' THEN 1 ELSE 0 END) AS delayed_count,
    SUM(CASE WHEN status = 'In Transit' THEN 1 ELSE 0 END) AS in_transit_count,
    ROUND((CAST(SUM(CASE WHEN status = 'Delayed' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(shipment_id)) * 100, 2) AS delay_rate_pct,
    ROUND((CAST(SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(shipment_id)) * 100, 2) AS fulfillment_rate_pct,
    SUM(quantity) AS total_units_shipped,
    ROUND(SUM(shipping_cost), 2) AS total_shipping_spend,
    ROUND(AVG(shipping_cost), 2) AS avg_cost_per_shipment,
    ROUND(SUM(shipping_cost) / NULLIF(SUM(quantity), 0), 2) AS freight_cost_per_unit
FROM fact_shipment
GROUP BY carrier
ORDER BY delay_rate_pct DESC;


-- =================================================================================================
-- 8. ROOT-CAUSE DECOMPOSITION OF SHIPMENT DELAY EXCEPTIONS
-- Purpose: Identify primary operational bottlenecks driving logistics delays
-- =================================================================================================
WITH DelayBreakdown AS (
    SELECT
        COALESCE(delay_reason, 'Unspecified / No Reason') AS delay_reason,
        COUNT(shipment_id) AS delayed_shipment_count,
        SUM(quantity) AS affected_unit_volume,
        SUM(shipping_cost) AS impacted_shipping_cost,
        AVG(total_weight_kg) AS avg_shipment_weight_kg
    FROM fact_shipment
    WHERE status = 'Delayed'
    GROUP BY delay_reason
)
SELECT
    delay_reason,
    delayed_shipment_count,
    ROUND((delayed_shipment_count / (SELECT CAST(SUM(delayed_shipment_count) AS FLOAT) FROM DelayBreakdown)) * 100, 2) AS delay_share_pct,
    affected_unit_volume,
    impacted_shipping_cost,
    ROUND(avg_shipment_weight_kg, 2) AS avg_shipment_weight_kg
FROM DelayBreakdown
ORDER BY delayed_shipment_count DESC;


-- =================================================================================================
-- 9. CUSTOMER CHANNEL ECONOMICS & DISCOUNT ELASTICITY
-- Purpose: Evaluate commercial profitability, discount burn, and net return across retail channels
-- =================================================================================================
SELECT
    c.customer_name,
    c.channel_type,
    c.country AS market_country,
    COUNT(s.sales_id) AS total_transactions,
    SUM(s.quantity_sold) AS total_units_sold,
    ROUND(SUM(s.gross_revenue), 2) AS gross_revenue,
    ROUND(SUM(s.discount_amount), 2) AS discount_allowance,
    ROUND((SUM(s.discount_amount) / NULLIF(SUM(s.gross_revenue), 0)) * 100, 2) AS avg_discount_rate_pct,
    ROUND(SUM(s.net_revenue), 2) AS net_revenue,
    ROUND(SUM(s.profit), 2) AS total_profit,
    ROUND((SUM(s.profit) / NULLIF(SUM(s.net_revenue), 0)) * 100, 2) AS net_margin_pct,
    ROUND(SUM(s.profit) / NULLIF(SUM(s.quantity_sold), 0), 2) AS profit_per_unit_sold
FROM fact_sales s
JOIN dim_customer c ON s.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name, c.channel_type, c.country
ORDER BY net_revenue DESC;


-- =================================================================================================
-- 10. CARRIER COST VS. RELIABILITY MATRIX (BENCHMARKING VALUE FOR MONEY)
-- Purpose: Classify carriers into Cost vs Reliability quadrants to optimize freight procurement
-- =================================================================================================
WITH CarrierBenchmarks AS (
    SELECT
        carrier,
        COUNT(shipment_id) AS total_trips,
        ROUND((CAST(SUM(CASE WHEN status = 'Delayed' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(shipment_id)) * 100, 2) AS delay_pct,
        ROUND(AVG(shipping_cost), 2) AS avg_cost,
        AVG(AVG(shipping_cost)) OVER () AS global_avg_cost,
        AVG(CAST(SUM(CASE WHEN status = 'Delayed' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(shipment_id) * 100) OVER () AS global_avg_delay_pct
    FROM fact_shipment
    GROUP BY carrier
)
SELECT
    carrier,
    total_trips,
    avg_cost,
    delay_pct,
    CASE
        WHEN avg_cost <= global_avg_cost AND delay_pct <= global_avg_delay_pct THEN 'High Value (Low Cost, High Reliability)'
        WHEN avg_cost > global_avg_cost AND delay_pct <= global_avg_delay_pct THEN 'Premium / Reliable (High Cost, High Reliability)'
        WHEN avg_cost <= global_avg_cost AND delay_pct > global_avg_delay_pct THEN 'Budget / Risk (Low Cost, High Delay)'
        ELSE 'Underperforming / High Cost Lag (High Cost, High Delay)'
    END AS carrier_strategic_quadrant
FROM CarrierBenchmarks
ORDER BY delay_pct ASC, avg_cost ASC;

-- =================================================================================================
-- END OF SCRIPT
-- =================================================================================================

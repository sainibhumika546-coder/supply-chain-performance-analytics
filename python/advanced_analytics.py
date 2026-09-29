"""
====================================================================================================
SUPPLY CHAIN PERFORMANCE & OPERATIONS ANALYTICS
Module: Advanced Analytical Modeling & Statistical Diagnostics
Author: Data Analytics Portfolio
====================================================================================================
"""

import pandas as pd
import numpy as np
import os

def run_supplier_risk_analytics(data_dir="data"):
    """Evaluates vendor lead times, variability, spend concentration, and quality scores."""
    proc = pd.read_csv(os.path.join(data_dir, "fact_procurement.csv"))
    sup = pd.read_csv(os.path.join(data_dir, "dim_supplier.csv"))
    
    merged = proc.merge(sup, on="supplier_id")
    
    summary = merged.groupby(["supplier_name", "country", "tier", "specialty"]).agg(
        total_orders=("procurement_id", "count"),
        total_units=("order_quantity", "sum"),
        total_spend=("total_cost", "sum"),
        avg_lead_time=("lead_time_days", "mean"),
        std_lead_time=("lead_time_days", "std"),
        p95_lead_time=("lead_time_days", lambda x: np.percentile(x, 95)),
        avg_quality=("quality_score", "mean"),
        min_quality=("quality_score", "min")
    ).reset_index()
    
    total_spend_all = summary["total_spend"].sum()
    summary["spend_share_pct"] = (summary["total_spend"] / total_spend_all) * 100
    
    # Calculate composite Supplier Risk Score (0 - 100, higher = higher risk)
    # Risk factors: Lead time volatility (35%), Quality deficit from 100 (40%), Spend concentration (25%)
    summary["risk_score"] = (
        (summary["std_lead_time"] / summary["std_lead_time"].max() * 35) +
        ((100 - summary["avg_quality"]) / (100 - summary["avg_quality"].min()) * 40) +
        (summary["spend_share_pct"] / summary["spend_share_pct"].max() * 25)
    ).round(1)
    
    summary = summary.sort_values("total_spend", ascending=False)
    print("\n" + "="*80)
    print("1. ADVANCED SUPPLIER RISK & CONCENTRATION MATRIX")
    print("="*80)
    print(summary[["supplier_name", "country", "spend_share_pct", "avg_lead_time", "std_lead_time", "p95_lead_time", "avg_quality", "risk_score"]].to_string(index=False))
    return summary

def run_inventory_stockout_audit(data_dir="data"):
    """Categorizes inventory positions into risk tiers and estimates capital at risk."""
    inv = pd.read_csv(os.path.join(data_dir, "fact_inventory.csv"))
    prod = pd.read_csv(os.path.join(data_dir, "dim_product.csv"))
    fac = pd.read_csv(os.path.join(data_dir, "dim_facility.csv"))
    
    merged = inv.merge(prod, on="product_id").merge(fac, on="facility_id")
    merged["inventory_value"] = merged["stock_level"] * merged["unit_cost"]
    
    # Define Risk Conditions
    conditions = [
        (merged["stock_level"] < merged["safety_stock_level"]),
        (merged["stock_level"] <= merged["reorder_point"]),
        (merged["stock_level"] > merged["safety_stock_level"] * 2.5)
    ]
    choices = ["Critical Stockout Risk", "Reorder Required", "Excess / Overstocked"]
    merged["health_status"] = np.select(conditions, choices, default="Healthy Buffer")
    
    audit = merged.groupby("health_status").agg(
        record_count=("inventory_id", "count"),
        total_units=("stock_level", "sum"),
        total_valuation=("inventory_value", "sum"),
        avg_safety_stock=("safety_stock_level", "mean"),
        avg_stock_level=("stock_level", "mean")
    ).reset_index()
    
    total_val = audit["total_valuation"].sum()
    audit["val_share_pct"] = (audit["total_valuation"] / total_val) * 100
    
    print("\n" + "="*80)
    print("2. INVENTORY HEALTH & CAPITAL ALLOCATION AUDIT")
    print("="*80)
    print(audit.sort_values("total_valuation", ascending=False).to_string(index=False))
    return merged, audit

def run_carrier_reliability_quadrant(data_dir="data"):
    """Evaluates carrier performance across freight cost, delay rate, and delay root causes."""
    ship = pd.read_csv(os.path.join(data_dir, "fact_shipment.csv"))
    
    carrier_summary = ship.groupby("carrier").agg(
        total_shipments=("shipment_id", "count"),
        delayed_shipments=("status", lambda x: (x == "Delayed").sum()),
        delivered_shipments=("status", lambda x: (x == "Delivered").sum()),
        delay_rate_pct=("status", lambda x: (x == "Delayed").mean() * 100),
        total_freight_cost=("shipping_cost", "sum"),
        avg_cost_per_shipment=("shipping_cost", "mean"),
        avg_weight_kg=("total_weight_kg", "mean")
    ).reset_index()
    
    global_avg_cost = carrier_summary["avg_cost_per_shipment"].mean()
    global_avg_delay = carrier_summary["delay_rate_pct"].mean()
    
    def classify_quadrant(row):
        if row["avg_cost_per_shipment"] <= global_avg_cost and row["delay_rate_pct"] <= global_avg_delay:
            return "Tier 1: High Value (Low Cost, High Reliability)"
        elif row["avg_cost_per_shipment"] > global_avg_cost and row["delay_rate_pct"] <= global_avg_delay:
            return "Tier 2: Premium (High Cost, High Reliability)"
        elif row["avg_cost_per_shipment"] <= global_avg_cost and row["delay_rate_pct"] > global_avg_delay:
            return "Tier 3: Budget Risk (Low Cost, High Delays)"
        else:
            return "Tier 4: Inefficient (High Cost, High Delays)"
            
    carrier_summary["strategic_quadrant"] = carrier_summary.apply(classify_quadrant, axis=1)
    
    print("\n" + "="*80)
    print("3. CARRIER RELIABILITY & COST STRATEGIC QUADRANT")
    print("="*80)
    print(carrier_summary.sort_values("delay_rate_pct", ascending=False)[["carrier", "total_shipments", "delay_rate_pct", "avg_cost_per_shipment", "strategic_quadrant"]].to_string(index=False))
    
    # Delay Root Cause Breakdown
    delayed = ship[ship["status"] == "Delayed"]
    reasons = delayed.groupby("delay_reason").agg(
        incident_count=("shipment_id", "count"),
        affected_units=("quantity", "sum"),
        impacted_cost=("shipping_cost", "sum")
    ).reset_index()
    reasons["incident_share_pct"] = (reasons["incident_count"] / reasons["incident_count"].sum()) * 100
    reasons = reasons.sort_values("incident_count", ascending=False)
    
    print("\n" + "="*80)
    print("4. SHIPMENT DELAY ROOT-CAUSE BREAKDOWN")
    print("="*80)
    print(reasons.to_string(index=False))
    return carrier_summary, reasons

def run_commercial_profitability_audit(data_dir="data"):
    """Analyzes product profitability, discount erosion, and channel return."""
    sales = pd.read_csv(os.path.join(data_dir, "fact_sales.csv"))
    prod = pd.read_csv(os.path.join(data_dir, "dim_product.csv"))
    cust = pd.read_csv(os.path.join(data_dir, "dim_customer.csv"))
    
    merged = sales.merge(prod, on="product_id").merge(cust, on="customer_id")
    
    # Channel Analysis
    channel_summary = merged.groupby("channel_type").agg(
        orders=("sales_id", "count"),
        units_sold=("quantity_sold", "sum"),
        gross_rev=("gross_revenue", "sum"),
        discounts=("discount_amount", "sum"),
        net_rev=("net_revenue", "sum"),
        cogs=("total_cost", "sum"),
        profit=("profit", "sum")
    ).reset_index()
    channel_summary["discount_rate_pct"] = (channel_summary["discounts"] / channel_summary["gross_rev"]) * 100
    channel_summary["net_margin_pct"] = (channel_summary["profit"] / channel_summary["net_rev"]) * 100
    
    print("\n" + "="*80)
    print("5. COMMERCIAL CHANNEL PERFORMANCE & MARGIN HEALTH")
    print("="*80)
    print(channel_summary.to_string(index=False))
    return channel_summary

if __name__ == "__main__":
    run_supplier_risk_analytics()
    run_inventory_stockout_audit()
    run_carrier_reliability_quadrant()
    run_commercial_profitability_audit()

"""
====================================================================================================
SUPPLY CHAIN PERFORMANCE & OPERATIONS ANALYTICS
Module: Exploratory Data Analysis & Integrity Validation
Author: Data Analytics Portfolio
====================================================================================================
"""

import pandas as pd
import numpy as np
import os
import glob

def load_all_datasets(data_dir="data"):
    """Loads and standardizes all tables from the data directory."""
    tables = {}
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
    for f in csv_files:
        name = os.path.splitext(os.path.basename(f))[0]
        tables[name] = pd.read_csv(f)
    return tables

def audit_data_integrity(tables):
    """Audits data types, missing values, and referential integrity across all tables."""
    print("="*80)
    print("DATASET INTEGRITY & HEALTH AUDIT")
    print("="*80)
    
    for name, df in sorted(tables.items()):
        null_counts = df.isnull().sum()
        total_nulls = null_counts.sum()
        print(f"\nTable: {name:<20} | Rows: {len(df):>6,} | Cols: {df.shape[1]:>2} | Nulls: {total_nulls:>5}")
        if total_nulls > 0:
            null_cols = null_counts[null_counts > 0]
            for c, cnt in null_cols.items():
                print(f"  -> Column '{c}': {cnt} nulls ({cnt/len(df)*100:.2f}%) [Note: Expected for non-delayed shipments]")

    print("\n" + "="*80)
    print("REFERENTIAL INTEGRITY CHECKS")
    print("="*80)
    
    # Check Foreign Keys
    p_ids = set(tables['dim_product']['product_id'])
    for fact in ['fact_procurement', 'fact_production', 'fact_inventory', 'fact_sales', 'fact_shipment']:
        if fact in tables:
            missing_p = set(tables[fact]['product_id']) - p_ids
            print(f"Foreign Key check: {fact}.product_id -> dim_product.product_id: {len(missing_p)} orphan keys")
            
    c_ids = set(tables['dim_customer']['customer_id'])
    for fact in ['fact_sales', 'fact_shipment']:
        if fact in tables:
            missing_c = set(tables[fact]['customer_id']) - c_ids
            print(f"Foreign Key check: {fact}.customer_id -> dim_customer.customer_id: {len(missing_c)} orphan keys")

    s_ids = set(tables['dim_supplier']['supplier_id'])
    missing_s = set(tables['fact_procurement']['supplier_id']) - s_ids
    print(f"Foreign Key check: fact_procurement.supplier_id -> dim_supplier.supplier_id: {len(missing_s)} orphan keys")

    f_ids = set(tables['dim_facility']['facility_id'])
    for fact in ['fact_production', 'fact_inventory']:
        if fact in tables:
            missing_f = set(tables[fact]['facility_id']) - f_ids
            print(f"Foreign Key check: {fact}.facility_id -> dim_facility.facility_id: {len(missing_f)} orphan keys")

def compute_executive_kpis(tables):
    """Computes global operational and financial KPIs."""
    sales = tables['fact_sales']
    procurement = tables['fact_procurement']
    production = tables['fact_production']
    inventory = tables['fact_inventory']
    shipment = tables['fact_shipment']
    products = tables['dim_product']
    
    # Commercial
    gross_rev = sales['gross_revenue'].sum()
    net_rev = sales['net_revenue'].sum()
    discounts = sales['discount_amount'].sum()
    cogs = sales['total_cost'].sum()
    profit = sales['profit'].sum()
    margin = (profit / net_rev) * 100
    units_sold = sales['quantity_sold'].sum()
    
    # Procurement
    proc_spend = procurement['total_cost'].sum()
    proc_units = procurement['order_quantity'].sum()
    avg_lead_time = procurement['lead_time_days'].mean()
    avg_quality = procurement['quality_score'].mean()
    
    # Production
    prod_units = production['quantity_produced'].sum()
    defects = production['defective_units'].sum()
    defect_rate = (defects / prod_units) * 100
    
    # Inventory
    inv_merged = inventory.merge(products[['product_id', 'unit_cost']], on='product_id')
    inv_valuation = (inv_merged['stock_level'] * inv_merged['unit_cost']).sum()
    inv_units = inv_merged['stock_level'].sum()
    
    # Logistics
    total_trips = len(shipment)
    delays = (shipment['status'] == 'Delayed').sum()
    delay_rate = (delays / total_trips) * 100
    delivered = (shipment['status'] == 'Delivered').sum()
    otif_rate = (delivered / total_trips) * 100
    freight_spend = shipment['shipping_cost'].sum()

    print("\n" + "="*80)
    print("EXECUTIVE SUPPLY CHAIN CONTROL TOWER — GLOBAL KPIS")
    print("="*80)
    print(f"  [Financial] Gross Revenue:            ${gross_rev:,.2f}")
    print(f"  [Financial] Net Revenue:              ${net_rev:,.2f}")
    print(f"  [Financial] Commercial Discounts:     ${discounts:,.2f} ({discounts/gross_rev*100:.2f}% discount rate)")
    print(f"  [Financial] Cost of Goods Sold (COGS):${cogs:,.2f}")
    print(f"  [Financial] Net Operating Profit:     ${profit:,.2f} ({margin:.2f}% net margin)")
    print(f"  [Commercial] Total Units Sold:        {units_sold:,} units across {len(sales):,} orders")
    print(f"  [Procurement] Total Vendor Spend:     ${proc_spend:,.2f} across {len(procurement):,} POs")
    print(f"  [Procurement] Average Vendor Lead Time:{avg_lead_time:.2f} days (Benchmark SLA: 10 days)")
    print(f"  [Procurement] Supplier Quality Index: {avg_quality:.2f} / 100")
    print(f"  [Manufacturing] Total Units Produced: {prod_units:,} units")
    print(f"  [Manufacturing] Overall Defect Rate:  {defect_rate:.3f}% ({defects:,} scrap units)")
    print(f"  [Inventory] Total Stock Level:        {inv_units:,} units across all DC/Plant snapshots")
    print(f"  [Inventory] Total Inventory Valuation:${inv_valuation:,.2f}")
    print(f"  [Logistics] Total Global Shipments:   {total_trips:,} shipments")
    print(f"  [Logistics] Delay Exception Rate:     {delay_rate:.2f}% ({delays:,} delayed dispatches)")
    print(f"  [Logistics] Delivery Fulfillment Rate:{otif_rate:.2f}% ({delivered:,} delivered)")
    print(f"  [Logistics] Total Freight Spend:      ${freight_spend:,.2f}")
    print("="*80)

if __name__ == "__main__":
    datasets = load_all_datasets()
    audit_data_integrity(datasets)
    compute_executive_kpis(datasets)

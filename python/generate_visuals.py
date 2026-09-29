"""
====================================================================================================
SUPPLY CHAIN PERFORMANCE & OPERATIONS ANALYTICS
Module: Professional Visualizations & Dashboard Asset Generator
Theme: Modern Dark Slate Enterprise Analytics (#0F172A base, #38BDF8 primary, #10B981 positive, #EF4444 alert)
====================================================================================================
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import pandas as pd
import numpy as np
import os

# Set global styles
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#334155'
plt.rcParams['axes.linewidth'] = 0.8

# Load datasets
sales = pd.read_csv("data/fact_sales.csv")
dates = pd.read_csv("data/dim_date.csv")
products = pd.read_csv("data/dim_product.csv")
suppliers = pd.read_csv("data/dim_supplier.csv")
procurement = pd.read_csv("data/fact_procurement.csv")
inventory = pd.read_csv("data/fact_inventory.csv")
facilities = pd.read_csv("data/dim_facility.csv")
shipments = pd.read_csv("data/fact_shipment.csv")
customers = pd.read_csv("data/dim_customer.csv")

os.makedirs("screenshots", exist_ok=True)

# --------------------------------------------------------------------------------------------------
# Helper: Setup Figure Canvas
# --------------------------------------------------------------------------------------------------
def create_canvas(title, subtitle, page_num=1, total_pages=6):
    fig = plt.figure(figsize=(16, 9), dpi=150, facecolor='#0F172A')
    
    # Header Banner
    ax_head = fig.add_axes([0.03, 0.90, 0.94, 0.08], facecolor='#1E293B')
    ax_head.axis('off')
    # Rounded box for header
    rect = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02,rounding_size=0.04", 
                                  facecolor='#1E293B', edgecolor='#334155', linewidth=1.2)
    ax_head.add_patch(rect)
    
    ax_head.text(0.02, 0.62, title, fontsize=16, fontweight='bold', color='#F8FAFC', va='center')
    ax_head.text(0.02, 0.25, subtitle, fontsize=10, color='#94A3B8', va='center')
    
    ax_head.text(0.98, 0.62, "SUPPLY CHAIN CONTROL TOWER", fontsize=11, fontweight='bold', color='#38BDF8', ha='right', va='center')
    ax_head.text(0.98, 0.25, f"PAGE {page_num} OF {total_pages} | ENTERPRISE BI", fontsize=9, color='#64748B', ha='right', va='center')
    
    return fig

def add_kpi_card(fig, bbox, title, value, subtext, status_color='#38BDF8'):
    """Adds a modern KPI card inside the canvas."""
    ax = fig.add_axes(bbox, facecolor='#1E293B')
    ax.axis('off')
    rect = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.03,rounding_size=0.05",
                                  facecolor='#1E293B', edgecolor='#334155', linewidth=1)
    ax.add_patch(rect)
    
    # Top accent bar
    accent = patches.Rectangle((0.05, 0.92), 0.90, 0.05, facecolor=status_color, edgecolor='none')
    ax.add_patch(accent)
    
    ax.text(0.08, 0.72, title.upper(), fontsize=8.5, fontweight='bold', color='#94A3B8')
    ax.text(0.08, 0.38, value, fontsize=16, fontweight='bold', color='#F8FAFC')
    ax.text(0.08, 0.16, subtext, fontsize=7.5, color='#64748B')
    return ax

# --------------------------------------------------------------------------------------------------
# PAGE 1: EXECUTIVE CONTROL TOWER
# --------------------------------------------------------------------------------------------------
def generate_page_1():
    fig = create_canvas("GLOBAL OPERATIONS & FINANCIAL CONTROL TOWER", 
                        "Executive multi-echelon visibility across Revenue, Profit, Procurement, Inventory Health & Logistics SLAs", 1, 6)
    
    # KPI Row
    add_kpi_card(fig, [0.03, 0.77, 0.145, 0.11], "Net Revenue", "$176.95M", "8.5K Orders | +5.4% YoY", "#38BDF8")
    add_kpi_card(fig, [0.188, 0.77, 0.145, 0.11], "Operating Profit", "$48.56M", "27.44% Net Margin", "#10B981")
    add_kpi_card(fig, [0.346, 0.77, 0.145, 0.11], "Procurement Spend", "$78.13M", "2.2K POs | 7 Global Vendors", "#818CF8")
    add_kpi_card(fig, [0.504, 0.77, 0.145, 0.11], "Avg Vendor Lead Time", "11.53 Days", "Target SLA: 10.0 Days", "#F59E0B")
    add_kpi_card(fig, [0.662, 0.77, 0.145, 0.11], "Inventory Valuation", "$108.77M", "159.9K Units in Buffer", "#38BDF8")
    add_kpi_card(fig, [0.820, 0.77, 0.145, 0.11], "On-Time Dispatch Rate", "92.36%", "7.64% Delay Rate (573 trips)", "#10B981")

    # Visual 1: Monthly Financial Trajectory (Revenue vs Profit)
    ax1 = fig.add_axes([0.03, 0.40, 0.55, 0.34], facecolor='#1E293B')
    sales_m = sales.merge(dates, on='date_key').groupby(['year', 'month', 'month_name']).agg(
        rev=('net_revenue', lambda x: x.sum() / 1e6),
        prof=('profit', lambda x: x.sum() / 1e6)
    ).reset_index()
    sales_m['period'] = sales_m['year'].astype(str) + '-' + sales_m['month'].astype(str).str.zfill(2)
    
    ax1.plot(sales_m['period'], sales_m['rev'], color='#38BDF8', marker='o', linewidth=2.2, label='Net Revenue ($M)')
    ax1.plot(sales_m['period'], sales_m['prof'], color='#10B981', marker='s', linewidth=2, label='Operating Profit ($M)')
    ax1.set_title("Monthly Revenue & Operating Profit Trajectory (2023 - 2024)", fontsize=11, fontweight='bold', color='#F8FAFC', pad=10)
    ax1.set_xticklabels(sales_m['period'], rotation=45, ha='right', fontsize=7.5, color='#94A3B8')
    ax1.tick_params(colors='#94A3B8')
    ax1.grid(True, linestyle='--', alpha=0.2, color='#64748B')
    ax1.legend(facecolor='#0F172A', edgecolor='#334155', labelcolor='#F8FAFC', fontsize=8.5)

    # Visual 2: Category Revenue Breakdown
    ax2 = fig.add_axes([0.62, 0.40, 0.35, 0.34], facecolor='#1E293B')
    cat_sales = sales.merge(products, on='product_id').groupby('category')['net_revenue'].sum() / 1e6
    cat_sales = cat_sales.sort_values(ascending=True)
    bars = ax2.barh(cat_sales.index, cat_sales.values, color=['#818CF8', '#38BDF8', '#34D399', '#F59E0B', '#F472B6'])
    ax2.set_title("Net Revenue by Product Category ($M)", fontsize=11, fontweight='bold', color='#F8FAFC', pad=10)
    ax2.tick_params(colors='#94A3B8', labelsize=8.5)
    ax2.grid(True, linestyle='--', alpha=0.2, color='#64748B', axis='x')
    for bar in bars:
        w = bar.get_width()
        ax2.text(w + 1, bar.get_y() + bar.get_height()/2, f"${w:.1f}M", va='center', fontsize=8, color='#F8FAFC')

    # Visual 3: Carrier On-Time Performance
    ax3 = fig.add_axes([0.03, 0.06, 0.46, 0.28], facecolor='#1E293B')
    carrier_perf = shipments.groupby('carrier').agg(
        total=('shipment_id', 'count'),
        delayed=('status', lambda x: (x == 'Delayed').sum())
    ).reset_index()
    carrier_perf['delay_pct'] = (carrier_perf['delayed'] / carrier_perf['total']) * 100
    carrier_perf = carrier_perf.sort_values('delay_pct', ascending=True)
    
    colors = ['#10B981' if x < 7.5 else '#F59E0B' if x < 9.0 else '#EF4444' for x in carrier_perf['delay_pct']]
    ax3.barh(carrier_perf['carrier'], carrier_perf['delay_pct'], color=colors)
    ax3.axvline(7.64, color='#38BDF8', linestyle='--', linewidth=1.5, label='Global Benchmark (7.64%)')
    ax3.set_title("Logistics Delay Rate by Carrier Partner (%)", fontsize=11, fontweight='bold', color='#F8FAFC', pad=10)
    ax3.tick_params(colors='#94A3B8', labelsize=8)
    ax3.grid(True, linestyle='--', alpha=0.2, color='#64748B', axis='x')
    ax3.legend(facecolor='#0F172A', edgecolor='#334155', labelcolor='#F8FAFC', fontsize=7.5)

    # Visual 4: Channel Profitability Margin Comparison
    ax4 = fig.add_axes([0.53, 0.06, 0.44, 0.28], facecolor='#1E293B')
    ch_sales = sales.merge(customers, on='customer_id').groupby('channel_type').agg(
        rev=('net_revenue', lambda x: x.sum() / 1e6),
        prof=('profit', lambda x: x.sum() / 1e6)
    ).reset_index()
    ch_sales['margin'] = (ch_sales['prof'] / ch_sales['rev']) * 100
    
    x = np.arange(len(ch_sales))
    width = 0.35
    ax4.bar(x - width/2, ch_sales['rev'], width, label='Net Revenue ($M)', color='#38BDF8')
    ax4.bar(x + width/2, ch_sales['prof'], width, label='Operating Profit ($M)', color='#10B981')
    ax4.set_xticks(x)
    ax4.set_xticklabels(ch_sales['channel_type'], fontsize=8.5, color='#94A3B8')
    ax4.set_title("Commercial Channel Revenue & Profit Contribution ($M)", fontsize=11, fontweight='bold', color='#F8FAFC', pad=10)
    ax4.tick_params(colors='#94A3B8', labelsize=8)
    ax4.grid(True, linestyle='--', alpha=0.2, color='#64748B', axis='y')
    ax4.legend(facecolor='#0F172A', edgecolor='#334155', labelcolor='#F8FAFC', fontsize=8)

    plt.savefig("screenshots/01_executive_control_tower.png", dpi=150, bbox_inches='tight')
    plt.savefig("screenshots/00_hero_dashboard.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated Page 1: 01_executive_control_tower.png and 00_hero_dashboard.png")

# --------------------------------------------------------------------------------------------------
# PAGE 2: PROCUREMENT & SUPPLIER PERFORMANCE
# --------------------------------------------------------------------------------------------------
def generate_page_2():
    fig = create_canvas("PROCUREMENT & SUPPLIER CONCENTRATION RISK", 
                        "Vendor spend allocation, lead time distribution, quality compliance & price variance audit", 2, 6)
    
    add_kpi_card(fig, [0.03, 0.77, 0.17, 0.11], "Procurement Spend", "$78.13M", "Total PO Expenditure", "#38BDF8")
    add_kpi_card(fig, [0.22, 0.77, 0.17, 0.11], "Units Procured", "129.2K", "Across 2,200 Batches", "#818CF8")
    add_kpi_card(fig, [0.41, 0.77, 0.17, 0.11], "Avg Lead Time", "11.53 Days", "Range: 4 to 20 Days", "#F59E0B")
    add_kpi_card(fig, [0.60, 0.77, 0.17, 0.11], "Quality Compliance", "96.63 / 100", "Min Quality: 85.0", "#10B981")
    add_kpi_card(fig, [0.79, 0.77, 0.18, 0.11], "Concentration Risk", "Top 3: 43.8%", "BOE, SEC, TSMC", "#EF4444")

    # Visual 1: Supplier Spend & Lead Time
    ax1 = fig.add_axes([0.03, 0.08, 0.45, 0.64], facecolor='#1E293B')
    sup_m = procurement.merge(suppliers, on='supplier_id').groupby('supplier_name').agg(
        spend=('total_cost', lambda x: x.sum() / 1e6),
        lead_time=('lead_time_days', 'mean'),
        quality=('quality_score', 'mean')
    ).reset_index().sort_values('spend', ascending=True)
    
    bars = ax1.barh(sup_m['supplier_name'], sup_m['spend'], color='#38BDF8')
    ax1.set_title("Total Procurement Spend by Supplier ($M)", fontsize=11, fontweight='bold', color='#F8FAFC', pad=10)
    ax1.tick_params(colors='#94A3B8', labelsize=8.5)
    ax1.grid(True, linestyle='--', alpha=0.2, color='#64748B', axis='x')
    for b in bars:
        w = b.get_width()
        ax1.text(w + 0.2, b.get_y() + b.get_height()/2, f"${w:.2f}M", va='center', fontsize=8, color='#F8FAFC')

    # Visual 2: Supplier Quality vs Lead Time Quadrant
    ax2 = fig.add_axes([0.52, 0.42, 0.45, 0.30], facecolor='#1E293B')
    scatter = ax2.scatter(sup_m['lead_time'], sup_m['quality'], s=sup_m['spend']*60, c='#10B981', alpha=0.8, edgecolors='#F8FAFC', linewidth=1.2)
    for _, row in sup_m.iterrows():
        ax2.annotate(row['supplier_name'].split()[0], (row['lead_time'], row['quality'] + 0.15), fontsize=7.5, color='#F8FAFC', ha='center')
    ax2.set_title("Supplier Lead Time vs Quality Score (Bubble Size = Spend)", fontsize=11, fontweight='bold', color='#F8FAFC', pad=10)
    ax2.set_xlabel("Average Lead Time (Days)", fontsize=8.5, color='#94A3B8')
    ax2.set_ylabel("Quality Index (0 - 100)", fontsize=8.5, color='#94A3B8')
    ax2.tick_params(colors='#94A3B8', labelsize=8)
    ax2.grid(True, linestyle='--', alpha=0.2, color='#64748B')

    # Visual 3: Lead Time by Sourcing Country
    ax3 = fig.add_axes([0.52, 0.08, 0.45, 0.26], facecolor='#1E293B')
    country_lt = procurement.merge(suppliers, on='supplier_id').groupby('country')['lead_time_days'].mean().sort_values(ascending=False)
    ax3.bar(country_lt.index, country_lt.values, color=['#EF4444', '#F59E0B', '#F59E0B', '#F59E0B', '#10B981', '#10B981'])
    ax3.set_title("Average Lead Time by Vendor Sourcing Geography (Days)", fontsize=11, fontweight='bold', color='#F8FAFC', pad=10)
    ax3.tick_params(colors='#94A3B8', labelsize=8)
    ax3.grid(True, linestyle='--', alpha=0.2, color='#64748B', axis='y')

    plt.savefig("screenshots/02_procurement_supplier_risk.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated Page 2: 02_procurement_supplier_risk.png")

# --------------------------------------------------------------------------------------------------
# PAGE 3: INVENTORY HEALTH & OPERATIONS
# --------------------------------------------------------------------------------------------------
def generate_page_3():
    fig = create_canvas("INVENTORY BUFFER HEALTH & PRODUCTION RELIABILITY", 
                        "Stockout vulnerability scoring, safety stock coverage, scrap defect rates & facility capacity", 3, 6)
    
    add_kpi_card(fig, [0.03, 0.77, 0.17, 0.11], "Total Buffer Units", "159.9K Units", "Recorded Across All DCs", "#38BDF8")
    add_kpi_card(fig, [0.22, 0.77, 0.17, 0.11], "Inventory Valuation", "$108.77M", "Based on Standard Unit Cost", "#818CF8")
    add_kpi_card(fig, [0.41, 0.77, 0.17, 0.11], "Stockout Risk Tiers", "25 DC Snapshots", "Stock < Safety Stock", "#EF4444")
    add_kpi_card(fig, [0.60, 0.77, 0.17, 0.11], "Overstocked Capital", "$15.69M", "135 Batches > 2.5x Buffer", "#F59E0B")
    add_kpi_card(fig, [0.79, 0.77, 0.18, 0.11], "Manufacturing Defect Rate", "0.629%", "24,102 Total Scrap Units", "#10B981")

    # Visual 1: Inventory Capital Allocation by Health Status
    ax1 = fig.add_axes([0.03, 0.08, 0.45, 0.64], facecolor='#1E293B')
    inv_m = inventory.merge(products, on='product_id')
    inv_m['val'] = inv_m['stock_level'] * inv_m['unit_cost']
    conditions = [
        (inv_m['stock_level'] < inv_m['safety_stock_level']),
        (inv_m['stock_level'] <= inv_m['reorder_point']),
        (inv_m['stock_level'] > inv_m['safety_stock_level'] * 2.5)
    ]
    choices = ['Critical Stockout Risk', 'Reorder Required', 'Excess / Overstocked']
    inv_m['status'] = np.select(conditions, choices, default='Healthy Buffer')
    
    stat_summary = inv_m.groupby('status')['val'].sum() / 1e6
    stat_summary = stat_summary.sort_values(ascending=True)
    colors = ['#EF4444' if 'Risk' in x else '#F59E0B' if 'Reorder' in x or 'Excess' in x else '#10B981' for x in stat_summary.index]
    
    bars = ax1.barh(stat_summary.index, stat_summary.values, color=colors)
    ax1.set_title("Capital Allocation by Inventory Health Position ($M)", fontsize=11, fontweight='bold', color='#F8FAFC', pad=10)
    ax1.tick_params(colors='#94A3B8', labelsize=8.5)
    ax1.grid(True, linestyle='--', alpha=0.2, color='#64748B', axis='x')
    for b in bars:
        w = b.get_width()
        ax1.text(w + 0.5, b.get_y() + b.get_height()/2, f"${w:.2f}M", va='center', fontsize=8, color='#F8FAFC')

    # Visual 2: Stock Level vs Reorder Point by Product
    ax2 = fig.add_axes([0.52, 0.42, 0.45, 0.30], facecolor='#1E293B')
    prod_inv = inv_m.groupby('product_name').agg(
        avg_stock=('stock_level', 'mean'),
        avg_reorder=('reorder_point', 'mean'),
        avg_safety=('safety_stock_level', 'mean')
    ).head(8)
    
    x = np.arange(len(prod_inv))
    ax2.bar(x - 0.2, prod_inv['avg_stock'], 0.4, label='Current Stock Level', color='#38BDF8')
    ax2.bar(x + 0.2, prod_inv['avg_reorder'], 0.4, label='Reorder Threshold', color='#F59E0B')
    ax2.set_xticks(x)
    ax2.set_xticklabels([name[:12] + '..' for name in prod_inv.index], rotation=30, ha='right', fontsize=7.5, color='#94A3B8')
    ax2.set_title("Current Stock vs Reorder Points (Top Products)", fontsize=11, fontweight='bold', color='#F8FAFC', pad=10)
    ax2.tick_params(colors='#94A3B8', labelsize=8)
    ax2.grid(True, linestyle='--', alpha=0.2, color='#64748B', axis='y')
    ax2.legend(facecolor='#0F172A', edgecolor='#334155', labelcolor='#F8FAFC', fontsize=7.5)

    # Visual 3: Manufacturing Defect Rates by Facility
    ax3 = fig.add_axes([0.52, 0.08, 0.45, 0.26], facecolor='#1E293B')
    fac_perf = pd.read_csv("data/fact_production.csv").merge(facilities, on='facility_id').groupby('facility_name').agg(
        total_prod=('quantity_produced', 'sum'),
        defects=('defective_units', 'sum')
    ).reset_index()
    fac_perf['defect_pct'] = (fac_perf['defects'] / fac_perf['total_prod']) * 100
    fac_perf = fac_perf.sort_values('defect_pct', ascending=False)
    
    ax3.bar(fac_perf['facility_name'], fac_perf['defect_pct'], color='#34D399')
    ax3.set_title("Scrap Defect Rate by Manufacturing Facility (%)", fontsize=11, fontweight='bold', color='#F8FAFC', pad=10)
    ax3.tick_params(colors='#94A3B8', labelsize=7.5)
    ax3.set_xticklabels(fac_perf['facility_name'], rotation=15, ha='right')
    ax3.grid(True, linestyle='--', alpha=0.2, color='#64748B', axis='y')

    plt.savefig("screenshots/03_inventory_operations_health.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated Page 3: 03_inventory_operations_health.png")

# --------------------------------------------------------------------------------------------------
# PAGE 4: LOGISTICS & CARRIER PERFORMANCE
# --------------------------------------------------------------------------------------------------
def generate_page_4():
    fig = create_canvas("LOGISTICS, FREIGHT ECONOMICS & CARRIER RELIABILITY", 
                        "Dispatch SLA tracking, carrier cost vs reliability matrix, and delay root-cause decomposition", 4, 6)
    
    add_kpi_card(fig, [0.03, 0.77, 0.17, 0.11], "Total Shipments", "7,500 Trips", "Global Freight Dispatches", "#38BDF8")
    add_kpi_card(fig, [0.22, 0.77, 0.17, 0.11], "Delivered Shipments", "5,647 Trips", "75.29% Delivered to Date", "#10B981")
    add_kpi_card(fig, [0.41, 0.77, 0.17, 0.11], "Delay Exception Count", "573 Trips", "7.64% Delay Exception Rate", "#EF4444")
    add_kpi_card(fig, [0.60, 0.77, 0.17, 0.11], "Total Freight Cost", "$19.42M", "Avg: $2,589 per Shipment", "#818CF8")
    add_kpi_card(fig, [0.79, 0.77, 0.18, 0.11], "Top Delay Driver", "Carrier Capacity", "15.71% of All Delayed Trips", "#F59E0B")

    # Visual 1: Delay Root Causes
    ax1 = fig.add_axes([0.03, 0.08, 0.45, 0.64], facecolor='#1E293B')
    delays = shipments[shipments['status'] == 'Delayed']['delay_reason'].value_counts()
    bars = ax1.barh(delays.index, delays.values, color='#F59E0B')
    ax1.set_title("Root-Cause Distribution of Delayed Shipments (Trip Count)", fontsize=11, fontweight='bold', color='#F8FAFC', pad=10)
    ax1.tick_params(colors='#94A3B8', labelsize=8.5)
    ax1.grid(True, linestyle='--', alpha=0.2, color='#64748B', axis='x')
    for b in bars:
        w = b.get_width()
        pct = (w / delays.sum()) * 100
        ax1.text(w + 1.5, b.get_y() + b.get_height()/2, f"{w} ({pct:.1f}%)", va='center', fontsize=8, color='#F8FAFC')

    # Visual 2: Carrier Cost vs Delay Scatter
    ax2 = fig.add_axes([0.52, 0.42, 0.45, 0.30], facecolor='#1E293B')
    carrier_agg = shipments.groupby('carrier').agg(
        delay_pct=('status', lambda x: (x == 'Delayed').mean() * 100),
        avg_cost=('shipping_cost', 'mean'),
        trips=('shipment_id', 'count')
    ).reset_index()
    
    ax2.scatter(carrier_agg['delay_pct'], carrier_agg['avg_cost'], s=carrier_agg['trips']/2, c='#38BDF8', alpha=0.8, edgecolors='#F8FAFC')
    for _, row in carrier_agg.iterrows():
        ax2.annotate(row['carrier'].split()[0], (row['delay_pct'], row['avg_cost'] + 25), fontsize=8, color='#F8FAFC')
    ax2.axvline(7.64, color='#EF4444', linestyle='--', alpha=0.6, label='Avg Delay (7.64%)')
    ax2.axhline(2589, color='#10B981', linestyle='--', alpha=0.6, label='Avg Freight ($2,589)')
    ax2.set_title("Carrier Strategic Matrix: Freight Cost vs Delay Rate %", fontsize=11, fontweight='bold', color='#F8FAFC', pad=10)
    ax2.set_xlabel("Delay Rate % (Lower is Better)", fontsize=8.5, color='#94A3B8')
    ax2.set_ylabel("Average Cost per Shipment ($)", fontsize=8.5, color='#94A3B8')
    ax2.tick_params(colors='#94A3B8', labelsize=8)
    ax2.grid(True, linestyle='--', alpha=0.2, color='#64748B')
    ax2.legend(facecolor='#0F172A', edgecolor='#334155', labelcolor='#F8FAFC', fontsize=7.5)

    # Visual 3: Freight Spend by Carrier
    ax3 = fig.add_axes([0.52, 0.08, 0.45, 0.26], facecolor='#1E293B')
    c_spend = (shipments.groupby('carrier')['shipping_cost'].sum() / 1e6).sort_values(ascending=False)
    ax3.bar(c_spend.index, c_spend.values, color='#818CF8')
    ax3.set_title("Total Freight Spend Allocated by Logistics Partner ($M)", fontsize=11, fontweight='bold', color='#F8FAFC', pad=10)
    ax3.tick_params(colors='#94A3B8', labelsize=7.5)
    ax3.set_xticklabels([c[:10] for c in c_spend.index], rotation=20, ha='right')
    ax3.grid(True, linestyle='--', alpha=0.2, color='#64748B', axis='y')

    plt.savefig("screenshots/04_logistics_carrier_performance.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated Page 4: 04_logistics_carrier_performance.png")

# --------------------------------------------------------------------------------------------------
# PAGE 5: SALES & COMMERCIAL PROFITABILITY
# --------------------------------------------------------------------------------------------------
def generate_page_5():
    fig = create_canvas("COMMERCIAL SALES & PRODUCT PROFITABILITY", 
                        "Revenue Pareto (80/20) curve, discount allowance impact, channel return & SKU margin contribution", 5, 6)
    
    add_kpi_card(fig, [0.03, 0.77, 0.17, 0.11], "Gross Revenue", "$186.86M", "Base List Price Value", "#38BDF8")
    add_kpi_card(fig, [0.22, 0.77, 0.17, 0.11], "Discounts Burn", "$9.92M", "5.31% Discount Rate", "#EF4444")
    add_kpi_card(fig, [0.41, 0.77, 0.17, 0.11], "Net Revenue", "$176.95M", "Post-Discount Realized", "#38BDF8")
    add_kpi_card(fig, [0.60, 0.77, 0.17, 0.11], "Total Net Profit", "$48.56M", "27.44% Margin on Net Rev", "#10B981")
    add_kpi_card(fig, [0.79, 0.77, 0.18, 0.11], "Pareto Top 4 SKUs", "43.7% Revenue", "S24 Ultra, Z Fold5, Z Flip5", "#818CF8")

    # Visual 1: Product Revenue & Profit Margin
    ax1 = fig.add_axes([0.03, 0.08, 0.50, 0.64], facecolor='#1E293B')
    prod_sales = sales.merge(products, on='product_id').groupby('product_name').agg(
        rev=('net_revenue', lambda x: x.sum() / 1e6),
        prof=('profit', lambda x: x.sum() / 1e6)
    ).reset_index().sort_values('rev', ascending=True)
    
    y = np.arange(len(prod_sales))
    ax1.barh(y - 0.2, prod_sales['rev'], 0.4, label='Net Revenue ($M)', color='#38BDF8')
    ax1.barh(y + 0.2, prod_sales['prof'], 0.4, label='Net Profit ($M)', color='#10B981')
    ax1.set_yticks(y)
    ax1.set_yticklabels(prod_sales['product_name'], fontsize=8, color='#94A3B8')
    ax1.set_title("Product Portfolio: Net Revenue vs Operating Profit ($M)", fontsize=11, fontweight='bold', color='#F8FAFC', pad=10)
    ax1.tick_params(colors='#94A3B8', labelsize=8)
    ax1.grid(True, linestyle='--', alpha=0.2, color='#64748B', axis='x')
    ax1.legend(facecolor='#0F172A', edgecolor='#334155', labelcolor='#F8FAFC', fontsize=8)

    # Visual 2: Channel Revenue & Profit
    ax2 = fig.add_axes([0.58, 0.42, 0.39, 0.30], facecolor='#1E293B')
    ch_rev = sales.merge(customers, on='customer_id').groupby('customer_name')['net_revenue'].sum() / 1e6
    ch_rev = ch_rev.sort_values(ascending=False)
    ax2.bar(ch_rev.index, ch_rev.values, color=['#38BDF8', '#818CF8', '#34D399', '#F59E0B', '#F472B6'])
    ax2.set_title("Net Revenue by Key Account / Platform ($M)", fontsize=11, fontweight='bold', color='#F8FAFC', pad=10)
    ax2.tick_params(colors='#94A3B8', labelsize=7.5)
    ax2.set_xticklabels(ch_rev.index, rotation=20, ha='right')
    ax2.grid(True, linestyle='--', alpha=0.2, color='#64748B', axis='y')

    # Visual 3: Discount vs Margin Scatter
    ax3 = fig.add_axes([0.58, 0.08, 0.39, 0.26], facecolor='#1E293B')
    disc_data = sales.sample(500, random_state=42)
    ax3.scatter(disc_data['discount_pct'], disc_data['profit_margin_pct'], color='#F472B6', alpha=0.5)
    ax3.set_title("Impact of Discount % on Transaction Profit Margin %", fontsize=11, fontweight='bold', color='#F8FAFC', pad=10)
    ax3.set_xlabel("Discount Applied (%)", fontsize=8.5, color='#94A3B8')
    ax3.set_ylabel("Realized Margin (%)", fontsize=8.5, color='#94A3B8')
    ax3.tick_params(colors='#94A3B8', labelsize=8)
    ax3.grid(True, linestyle='--', alpha=0.2, color='#64748B')

    plt.savefig("screenshots/05_commercial_sales_profitability.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated Page 5: 05_commercial_sales_profitability.png")

# --------------------------------------------------------------------------------------------------
# PAGE 6: EXECUTIVE INSIGHTS MATRIX
# --------------------------------------------------------------------------------------------------
def generate_page_6():
    fig = create_canvas("STRATEGIC INSIGHTS & ACTIONABLE RECOMMENDATIONS MATRIX", 
                        "Executive synthesis of operational bottlenecks, financial risks, and management mitigation roadmap", 6, 6)
    
    # Render structured insight cards
    insights = [
        {
            "domain": "PROCUREMENT & LEAD TIME",
            "obs": "Supplier Lead Times Exhibit 8-Day Delivery Spread",
            "evid": "Chinese/Japanese suppliers average 12.4 days vs Vietnam at 9.39 days. SLA benchmark is 10.0 days.",
            "imp": "Creates buffer uncertainty and risks replenishment stockouts in Western distribution centers.",
            "act": "Renegotiate Tier 1 SLAs with guaranteed expedite windows and dual-source critical IC components.",
            "color": "#F59E0B"
        },
        {
            "domain": "INVENTORY BUFFER MANAGEMENT",
            "obs": "$15.69M Capital Locked in Overstocked Inventory",
            "evid": "135 warehouse snapshots hold stock >2.5x safety stock, while 25 snapshots are below critical buffer.",
            "imp": "High holding costs and cash drag alongside localized stockout vulnerability for high-margin SKUs.",
            "act": "Implement dynamic reorder trigger algorithms and inter-facility stock rebalancing across regional DCs.",
            "color": "#EF4444"
        },
        {
            "domain": "LOGISTICS & CARRIER SLA",
            "obs": "Maersk & DHL Show Elevated Delay Rates (>8.0%)",
            "evid": "Carrier Capacity (15.7%) and Documentation (13.6%) represent ~30% of all delay exceptions.",
            "imp": "Damages customer delivery commitments and inflates indirect detention/demurrage expenses.",
            "act": "Reallocate volume toward C.H. Robinson (6.92% delay) and digitize automated customs pre-clearance.",
            "color": "#38BDF8"
        },
        {
            "domain": "COMMERCIAL & MARGIN OPTIMIZATION",
            "obs": "Discounts Eroded $9.92M (5.31%) in Gross Margin",
            "evid": "Online marketplace channels receive highest discounting but generate 27.51% net margin.",
            "imp": "Discounts on flagship smartphones (S24 Ultra / Z Fold5) sacrifice margin without incremental volume lift.",
            "act": "Establish strict discount caps on high-demand premium tier SKUs and bundle accessories to protect margin.",
            "color": "#10B981"
        }
    ]

    positions = [
        [0.03, 0.48, 0.45, 0.38],
        [0.52, 0.48, 0.45, 0.38],
        [0.03, 0.06, 0.45, 0.38],
        [0.52, 0.06, 0.45, 0.38]
    ]

    for data, pos in zip(insights, positions):
        ax = fig.add_axes(pos, facecolor='#1E293B')
        ax.axis('off')
        rect = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.03,rounding_size=0.04",
                                      facecolor='#1E293B', edgecolor='#334155', linewidth=1.2)
        ax.add_patch(rect)
        
        # Header banner inside card
        card_hdr = patches.Rectangle((0.03, 0.88), 0.94, 0.09, facecolor=data['color'], alpha=0.2, edgecolor='none')
        ax.add_patch(card_hdr)
        ax.text(0.06, 0.92, data['domain'], fontsize=9, fontweight='bold', color=data['color'])
        
        ax.text(0.06, 0.78, data['obs'], fontsize=11, fontweight='bold', color='#F8FAFC')
        
        # Details
        ax.text(0.06, 0.62, "EVIDENCE:", fontsize=8, fontweight='bold', color='#38BDF8')
        ax.text(0.06, 0.52, data['evid'], fontsize=8, color='#CBD5E1', wrap=True)
        
        ax.text(0.06, 0.38, "BUSINESS IMPACT:", fontsize=8, fontweight='bold', color='#F59E0B')
        ax.text(0.06, 0.28, data['imp'], fontsize=8, color='#CBD5E1', wrap=True)
        
        ax.text(0.06, 0.16, "RECOMMENDED ACTION:", fontsize=8, fontweight='bold', color='#10B981')
        ax.text(0.06, 0.06, data['act'], fontsize=8, color='#CBD5E1', wrap=True)

    plt.savefig("screenshots/06_executive_insights_matrix.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Generated Page 6: 06_executive_insights_matrix.png")

if __name__ == "__main__":
    generate_page_1()
    generate_page_2()
    generate_page_3()
    generate_page_4()
    generate_page_5()
    generate_page_6()

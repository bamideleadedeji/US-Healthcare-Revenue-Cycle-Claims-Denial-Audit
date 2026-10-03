import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration & Styling
st.set_page_config(
    page_title="HealthRevenuePro USA | Claims Denial & Revenue Assurance Engine",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #0F172A; }
    .sub-header { font-size: 1.1rem; color: #475569; margin-bottom: 1.5rem; }
    </style>
""", unsafe_allow_html=True)

# Sidebar Operational Controls
st.sidebar.title("HealthRevenuePro USA")
st.sidebar.caption("Hospital RCM & Claims Revenue Assurance (US Standards)")

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Hospital Parameters")
hospital_beds = st.sidebar.number_input("Hospital Bed Capacity", min_value=10, max_value=2000, value=250, step=25)
monthly_claims_volume = st.sidebar.number_input("Monthly Billed Claims Count", min_value=100, max_value=50000, value=2500, step=250)
avg_claim_value = st.sidebar.number_input("Average Claim Value ($)", min_value=100.0, max_value=25000.0, value=3200.0, step=100.0)

st.sidebar.markdown("---")
st.sidebar.subheader("💵 Payer & Appeal Overheads")
avg_appeal_cost = st.sidebar.number_input("Cost to Appeal Denied Claim ($)", min_value=10.0, max_value=500.0, value=45.0, step=5.0)
appeal_success_rate = st.sidebar.slider("Estimated Appeal Recovery Success (%)", min_value=10.0, max_value=90.0, value=42.0, step=1.0)

# Main Title Header
st.markdown('<div class="main-header">🏥 HealthRevenuePro USA: Claims Denial & Revenue Assurance Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Executive RCM analytics, ICD-10/CPT coding audit, and insurance claim leakage recovery suite for US health systems.</div>', unsafe_allow_html=True)

# Core Analytics Calculation
payers = ["Medicare", "Medicaid", "Blue Cross Blue Shield", "UnitedHealth", "Aetna", "Humana"]
denial_reasons = ["Coding Mismatch (ICD-10/CPT)", "Prior Authorization Missing", "Incomplete Documentation", "Duplicate Claim", "Coverage Terminated", "Timely Filing Limit Exceeded"]

total_billed = monthly_claims_volume * avg_claim_value
industry_denial_rate = 11.2 # US National Average ~11%
denied_claims_count = int(monthly_claims_volume * (industry_denial_rate / 100.0))
gross_denied_revenue = denied_claims_count * avg_claim_value

total_appeal_costs = denied_claims_count * avg_appeal_cost
recovered_revenue = gross_denied_revenue * (appeal_success_rate / 100.0)
net_recovered_revenue = recovered_revenue - total_appeal_costs
unrecoverable_leakage = gross_denied_revenue - recovered_revenue

# Executive KPI Dashboard
st.subheader("📊 Executive RCM Financial Leakage Summary")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Billed Claims", f"${total_billed:,.2f}", f"{monthly_claims_volume:,} Claims")
col2.metric("Gross Denied Revenue", f"${gross_denied_revenue:,.2f}", f"{industry_denial_rate}% Denial Rate")
col3.metric("Net Recoverable Revenue", f"${net_recovered_revenue:,.2f}", f"{appeal_success_rate}% Appeal Win Rate")
col4.metric("Permanent Revenue Leakage", f"${unrecoverable_leakage:,.2f}", "Write-Off Risk")

st.markdown("---")

col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("💡 Denial Root Cause Breakdown")
    reasons_df = pd.DataFrame({
        "Denial Category": denial_reasons,
        "Share (%)": [32.0, 24.0, 18.0, 12.0, 8.0, 6.0]
    })
    reasons_df["Lost Revenue ($)"] = (gross_denied_revenue * (reasons_df["Share (%)"] / 100.0)).round(2)
    reasons_df["Recoverable Amount ($)"] = (reasons_df["Lost Revenue ($)"] * (appeal_success_rate / 100.0)).round(2)
    
    st.dataframe(reasons_df.sort_values(by="Lost Revenue ($)", ascending=False), use_container_width=True)

with col_right:
    st.subheader("📈 Payer Leakage Exposure ($)")
    payer_df = pd.DataFrame({
        "Commercial Payer": payers,
        "Denied Dollars ($)": [gross_denied_revenue * w for w in [0.30, 0.22, 0.20, 0.14, 0.08, 0.06]]
    })
    st.bar_chart(payer_df.set_index("Commercial Payer"))

# Export Suite
st.markdown("---")
st.subheader("📄 Commercial Audit Export Suite")

col_exp1, col_exp2 = st.columns(2)

with col_exp1:
    csv_buffer = reasons_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Claims Denial Audit Matrix (CSV)", data=csv_buffer, file_name="healthrevenuepro_us_audit.csv", mime="text/csv", use_container_width=True)

with col_exp2:
    summary_report = f"""HEALTHREVENUEPRO USA - HOSPITAL REVENUE ASSURANCE AUDIT
==================================================================
Facility Profile: {hospital_beds} Beds | Monthly Billed Claims: {monthly_claims_volume:,}
Total Billed Claims Revenue: ${total_billed:,.2f}

CLAIMS DENIAL & LEAKAGE METRICS:
- National Denial Rate Baseline: {industry_denial_rate}%
- Monthly Denied Claims Volume: {denied_claims_count:,} Claims
- GROSS REVENUE LOST TO DENIALS: ${gross_denied_revenue:,.2f}

RECOVERY & APPEAL PERFORMANCE:
- Appeal Cost Overhead: ${total_appeal_costs:,.2f}
- Projected Revenue Recovery ({appeal_success_rate}% success): ${recovered_revenue:,.2f}
- NET RECOVERABLE REVENUE AUDIT: ${net_recovered_revenue:,.2f}
- PERMANENT WRITE-OFF EXPOSURE: ${unrecoverable_leakage:,.2f}
==================================================================
Generated via HealthRevenuePro USA Suite
"""
    st.download_button(" Download Executive RCM Audit Summary (TXT)", data=summary_report, file_name="healthrevenuepro_executive_audit.txt", mime="text/plain", use_container_width=True)

"""
Net Yield Simulator Pro - Redesigned Layout
Three tables only: Summary, XIRR, Rate Breakdown
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import plotly.graph_objects as go
from io import BytesIO
import xlsxwriter
import warnings
warnings.filterwarnings('ignore')

# Try to import numpy-financial, fallback if not available
try:
    import numpy_financial as npf
    HAS_NPF = True
except ImportError:
    HAS_NPF = False

# Page Configuration
st.set_page_config(
    page_title="Net Yield Simulator Pro",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Keep the same styling but remove header styles
st.markdown("""
<style>
    /* Import Google Fonts and Material Icons */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
    
    /* ==================== GLOBAL STYLES ==================== */
    * { 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* Main App Background */
    .stApp {
        background-color: #f5f7fa !important;
    }
    
    .main {
        background-color: #f5f7fa !important;
    }
    
    .main .block-container {
        background-color: #f5f7fa !important;
        padding: 2rem 3rem !important;
        max-width: 1400px !important;
    }
    
    /* ==================== SIDEBAR STYLING ==================== */
    section[data-testid="stSidebar"] {
        background-color: #e8ebf0 !important;
        border-right: 1px solid #d1d5db !important;
        transition: all 0.3s ease !important;
        width: 420px !important;  /* Increased by 20% from ~350px default */
        min-width: 420px !important;
    }
    
    section[data-testid="stSidebar"] > div:first-child {
        background-color: #e8ebf0 !important;
        padding-top: 2rem !important;
        width: 420px !important;  /* Match the sidebar width */
    }
    
    /* Fix the collapse/expand arrow icon */
    button[kind="header"] {
        color: #4b5563 !important;
    }
    
    /* Replace text fallback with arrow symbols */
    button[kind="header"]:before {
        content: "◀" !important;
        font-size: 1.2rem !important;
        color: #4b5563 !important;
    }
    
    section[data-testid="stSidebar"][aria-expanded="false"] button[kind="header"]:before {
        content: "▶" !important;
    }
    
    /* Hide the fallback text completely */
    button[kind="header"] {
        font-size: 0 !important;
        overflow: hidden !important;
    }
    
    /* Ensure button is visible and clickable */
    button[kind="header"] {
        width: 32px !important;
        height: 32px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 0 !important;
    }
    
    /* Hide any keyboard_double_arrow text */
    .material-icons-outlined {
        display: none !important;
    }
    
    /* Sidebar Headers */
    section[data-testid="stSidebar"] h3 {
        color: #1f2937 !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        margin-bottom: 1.5rem !important;
        margin-top: 0 !important;
    }
    
    section[data-testid="stSidebar"] h4 {
        color: #1f2937 !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* Sidebar Labels */
    section[data-testid="stSidebar"] label {
        color: #4b5563 !important;
        font-weight: 500 !important;
        font-size: 0.8125rem !important;
    }
    
    /* Sidebar Input Fields */
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] select {
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 6px !important;
        color: #1f2937 !important;
        font-size: 0.875rem !important;
        padding: 0.5rem 0.75rem !important;
    }
    
    /* Sidebar Selectbox */
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 6px !important;
    }
    
    /* Sidebar Info Boxes */
    section[data-testid="stSidebar"] .stAlert {
        background-color: #dde3eb !important;
        border: 1px solid #c2cad6 !important;
        border-radius: 6px !important;
        color: #1f2937 !important;
        padding: 0.75rem !important;
        font-size: 0.8125rem !important;
    }
    
    /* Sidebar Dividers */
    section[data-testid="stSidebar"] hr {
        border: none !important;
        height: 1px !important;
        background-color: #d1d5db !important;
        margin: 1.5rem 0 !important;
    }
    
    /* ==================== TABLE STYLES ==================== */
    h3 {
        color: #111827 !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
        margin-top: 0 !important;
    }
    
    /* ==================== DATAFRAMES ==================== */
    .stDataFrame {
        border: 1px solid #e5e7eb !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }
    
    .stDataFrame table {
        background-color: #ffffff !important;
    }
    
    .stDataFrame thead tr th {
        background-color: #f9fafb !important;
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.8125rem !important;
        border-bottom: 2px solid #e5e7eb !important;
        padding: 0.75rem 1rem !important;
    }
    
    .stDataFrame tbody tr {
        border-bottom: 1px solid #f3f4f6 !important;
    }
    
    .stDataFrame tbody td {
        color: #1f2937 !important;
        font-size: 0.875rem !important;
        padding: 0.75rem 1rem !important;
    }
    
    .stDataFrame tbody tr:hover {
        background-color: #f9fafb !important;
    }
    
    /* ==================== EXPANDERS ==================== */
    .streamlit-expanderHeader {
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        color: #374151 !important;
        font-weight: 600 !important;
        padding: 0.75rem 1rem !important;
    }
    
    .streamlit-expanderContent {
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        padding: 1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Real Rate Index Table Data from Excel
@st.cache_data  
def load_rate_index_table():
    """Load embedded rate index table data from Excel"""
    rate_data = [
        {'Floating Ref': '1M', 'M': 1.0, 'LAST_PRICE': 0.039925, 'Custodian': 'DB', 'CoF v SOFR': 0.0, 'Swap Cost': 0.0, 'Loan Spread': 0.0068},
        {'Floating Ref': '1M', 'M': 2.0, 'LAST_PRICE': 0.0393299, 'Custodian': 'DB', 'CoF v SOFR': 0.0, 'Swap Cost': 0.0, 'Loan Spread': 0.0068},
        {'Floating Ref': '3M', 'M': 3.0, 'LAST_PRICE': 0.0388755, 'Custodian': 'DB', 'CoF v SOFR': 0.0, 'Swap Cost': 0.0, 'Loan Spread': 0.0068},
        {'Floating Ref': '3M', 'M': 4.0, 'LAST_PRICE': 0.03848, 'Custodian': 'DB', 'CoF v SOFR': 0.0, 'Swap Cost': 0.0, 'Loan Spread': 0.0068},
        {'Floating Ref': '3M', 'M': 5.0, 'LAST_PRICE': 0.0381285, 'Custodian': 'DB', 'CoF v SOFR': 0.0, 'Swap Cost': 0.0, 'Loan Spread': 0.0068},
        {'Floating Ref': '6M', 'M': 6.0, 'LAST_PRICE': 0.0378526, 'Custodian': 'DB', 'CoF v SOFR': 0.0, 'Swap Cost': 0.0, 'Loan Spread': 0.0068},
        {'Floating Ref': '3M', 'M': 7.0, 'LAST_PRICE': 0.037563, 'Custodian': 'DB', 'CoF v SOFR': 0.0, 'Swap Cost': 0.0, 'Loan Spread': 0.0068},
        {'Floating Ref': '3M', 'M': 8.0, 'LAST_PRICE': 0.0372395, 'Custodian': 'DB', 'CoF v SOFR': 0.0, 'Swap Cost': 0.0, 'Loan Spread': 0.0068},
        {'Floating Ref': '9M', 'M': 9.0, 'LAST_PRICE': 0.0369332, 'Custodian': 'DB', 'CoF v SOFR': 0.0, 'Swap Cost': 0.0, 'Loan Spread': 0.0068},
        {'Floating Ref': '3M', 'M': 10.0, 'LAST_PRICE': 0.0365935, 'Custodian': 'DB', 'CoF v SOFR': 0.0, 'Swap Cost': 0.0, 'Loan Spread': 0.0068},
        {'Floating Ref': '3M', 'M': 11.0, 'LAST_PRICE': 0.0362817, 'Custodian': 'DB', 'CoF v SOFR': 0.0, 'Swap Cost': 0.0, 'Loan Spread': 0.0068},
        {'Floating Ref': '12M', 'M': 12.0, 'LAST_PRICE': 0.035995, 'Custodian': 'DB', 'CoF v SOFR': 0.0, 'Swap Cost': 0.0, 'Loan Spread': 0.0068},
        # SG Data
        {'Floating Ref': '1M', 'M': 1.0, 'LAST_PRICE': 0.039925, 'Custodian': 'SG', 'CoF v SOFR': 0.002, 'Swap Cost': 0.0, 'Loan Spread': 0.0045},
        {'Floating Ref': '1M', 'M': 2.0, 'LAST_PRICE': 0.0393299, 'Custodian': 'SG', 'CoF v SOFR': 0.002, 'Swap Cost': 0.0, 'Loan Spread': 0.0045},
        {'Floating Ref': '3M', 'M': 3.0, 'LAST_PRICE': 0.0388755, 'Custodian': 'SG', 'CoF v SOFR': 0.002, 'Swap Cost': 0.0, 'Loan Spread': 0.0045},
        {'Floating Ref': '3M', 'M': 4.0, 'LAST_PRICE': 0.03848, 'Custodian': 'SG', 'CoF v SOFR': 0.002, 'Swap Cost': 0.0008, 'Loan Spread': 0.0045},
        {'Floating Ref': '3M', 'M': 5.0, 'LAST_PRICE': 0.0381285, 'Custodian': 'SG', 'CoF v SOFR': 0.002, 'Swap Cost': 0.0008, 'Loan Spread': 0.0045},
        {'Floating Ref': '6M', 'M': 6.0, 'LAST_PRICE': 0.0378526, 'Custodian': 'SG', 'CoF v SOFR': 0.002, 'Swap Cost': 0.0008, 'Loan Spread': 0.0045},
        {'Floating Ref': '3M', 'M': 7.0, 'LAST_PRICE': 0.037563, 'Custodian': 'SG', 'CoF v SOFR': 0.002, 'Swap Cost': 0.0008, 'Loan Spread': 0.0045},
        {'Floating Ref': '3M', 'M': 8.0, 'LAST_PRICE': 0.0372395, 'Custodian': 'SG', 'CoF v SOFR': 0.002, 'Swap Cost': 0.0008, 'Loan Spread': 0.0045},
        {'Floating Ref': '9M', 'M': 9.0, 'LAST_PRICE': 0.0369332, 'Custodian': 'SG', 'CoF v SOFR': 0.002, 'Swap Cost': 0.0008, 'Loan Spread': 0.0045},
        {'Floating Ref': '3M', 'M': 10.0, 'LAST_PRICE': 0.0365935, 'Custodian': 'SG', 'CoF v SOFR': 0.002, 'Swap Cost': 0.0008, 'Loan Spread': 0.0045},
        {'Floating Ref': '3M', 'M': 11.0, 'LAST_PRICE': 0.0362817, 'Custodian': 'SG', 'CoF v SOFR': 0.002, 'Swap Cost': 0.0008, 'Loan Spread': 0.0045},
        {'Floating Ref': '12M', 'M': 12.0, 'LAST_PRICE': 0.035995, 'Custodian': 'SG', 'CoF v SOFR': 0.002, 'Swap Cost': 0.0008, 'Loan Spread': 0.0045},
        # Barc Data  
        {'Floating Ref': '1M', 'M': 1.0, 'LAST_PRICE': 0.039925, 'Custodian': 'Barc', 'CoF v SOFR': 0.001, 'Swap Cost': 0.0005, 'Loan Spread': 0.0065},
        {'Floating Ref': '1M', 'M': 2.0, 'LAST_PRICE': 0.0393299, 'Custodian': 'Barc', 'CoF v SOFR': 0.001, 'Swap Cost': 0.0005, 'Loan Spread': 0.0065},
        {'Floating Ref': '3M', 'M': 3.0, 'LAST_PRICE': 0.0388755, 'Custodian': 'Barc', 'CoF v SOFR': 0.001, 'Swap Cost': 0.0005, 'Loan Spread': 0.0065},
        {'Floating Ref': '3M', 'M': 4.0, 'LAST_PRICE': 0.03848, 'Custodian': 'Barc', 'CoF v SOFR': 0.001, 'Swap Cost': 0.0005, 'Loan Spread': 0.0065},
        {'Floating Ref': '3M', 'M': 5.0, 'LAST_PRICE': 0.0381285, 'Custodian': 'Barc', 'CoF v SOFR': 0.001, 'Swap Cost': 0.0005, 'Loan Spread': 0.0065},
        {'Floating Ref': '6M', 'M': 6.0, 'LAST_PRICE': 0.0378526, 'Custodian': 'Barc', 'CoF v SOFR': 0.001, 'Swap Cost': 0.0005, 'Loan Spread': 0.0065},
        {'Floating Ref': '3M', 'M': 7.0, 'LAST_PRICE': 0.037563, 'Custodian': 'Barc', 'CoF v SOFR': 0.001, 'Swap Cost': 0.0005, 'Loan Spread': 0.0065},
        {'Floating Ref': '3M', 'M': 8.0, 'LAST_PRICE': 0.0372395, 'Custodian': 'Barc', 'CoF v SOFR': 0.001, 'Swap Cost': 0.0005, 'Loan Spread': 0.0065},
        {'Floating Ref': '9M', 'M': 9.0, 'LAST_PRICE': 0.0369332, 'Custodian': 'Barc', 'CoF v SOFR': 0.001, 'Swap Cost': 0.0005, 'Loan Spread': 0.0065},
        {'Floating Ref': '3M', 'M': 10.0, 'LAST_PRICE': 0.0365935, 'Custodian': 'Barc', 'CoF v SOFR': 0.001, 'Swap Cost': 0.0005, 'Loan Spread': 0.0065},
        {'Floating Ref': '3M', 'M': 11.0, 'LAST_PRICE': 0.0362817, 'Custodian': 'Barc', 'CoF v SOFR': 0.001, 'Swap Cost': 0.0005, 'Loan Spread': 0.0065},
        {'Floating Ref': '12M', 'M': 12.0, 'LAST_PRICE': 0.035995, 'Custodian': 'Barc', 'CoF v SOFR': 0.001, 'Swap Cost': 0.0005, 'Loan Spread': 0.0065},
        # CAI Data
        {'Floating Ref': '1M', 'M': 1.0, 'LAST_PRICE': 0.039925, 'Custodian': 'CAI', 'CoF v SOFR': 0.0025, 'Swap Cost': 0.0, 'Loan Spread': 0.0045},
        {'Floating Ref': '1M', 'M': 2.0, 'LAST_PRICE': 0.0393299, 'Custodian': 'CAI', 'CoF v SOFR': 0.0025, 'Swap Cost': 0.0, 'Loan Spread': 0.0045},
        {'Floating Ref': '3M', 'M': 3.0, 'LAST_PRICE': 0.0388755, 'Custodian': 'CAI', 'CoF v SOFR': 0.0025, 'Swap Cost': 0.0, 'Loan Spread': 0.0045},
        {'Floating Ref': '3M', 'M': 4.0, 'LAST_PRICE': 0.03848, 'Custodian': 'CAI', 'CoF v SOFR': 0.0025, 'Swap Cost': 0.0003, 'Loan Spread': 0.0045},
        {'Floating Ref': '3M', 'M': 5.0, 'LAST_PRICE': 0.0381285, 'Custodian': 'CAI', 'CoF v SOFR': 0.0025, 'Swap Cost': 0.0003, 'Loan Spread': 0.0045},
        {'Floating Ref': '6M', 'M': 6.0, 'LAST_PRICE': 0.0378526, 'Custodian': 'CAI', 'CoF v SOFR': 0.0025, 'Swap Cost': 0.0003, 'Loan Spread': 0.0045},
        {'Floating Ref': '3M', 'M': 7.0, 'LAST_PRICE': 0.037563, 'Custodian': 'CAI', 'CoF v SOFR': 0.0025, 'Swap Cost': 0.0003, 'Loan Spread': 0.0045},
        {'Floating Ref': '3M', 'M': 8.0, 'LAST_PRICE': 0.0372395, 'Custodian': 'CAI', 'CoF v SOFR': 0.0025, 'Swap Cost': 0.0003, 'Loan Spread': 0.0045},
        {'Floating Ref': '9M', 'M': 9.0, 'LAST_PRICE': 0.0369332, 'Custodian': 'CAI', 'CoF v SOFR': 0.0025, 'Swap Cost': 0.0003, 'Loan Spread': 0.0045},
        {'Floating Ref': '3M', 'M': 10.0, 'LAST_PRICE': 0.0365935, 'Custodian': 'CAI', 'CoF v SOFR': 0.0025, 'Swap Cost': 0.0003, 'Loan Spread': 0.0045},
        {'Floating Ref': '3M', 'M': 11.0, 'LAST_PRICE': 0.0362817, 'Custodian': 'CAI', 'CoF v SOFR': 0.0025, 'Swap Cost': 0.0003, 'Loan Spread': 0.0045},
        {'Floating Ref': '12M', 'M': 12.0, 'LAST_PRICE': 0.035995, 'Custodian': 'CAI', 'CoF v SOFR': 0.0025, 'Swap Cost': 0.0003, 'Loan Spread': 0.0045}
    ]
    
    return pd.DataFrame(rate_data)

# Utility Functions
def calculate_workday(trade_date, days_to_settle):
    """Calculate settlement date skipping weekends"""
    current_date = trade_date
    days_added = 0
    while days_added < days_to_settle:
        current_date += timedelta(days=1)
        if current_date.weekday() < 5:  # Monday = 0, Friday = 4
            days_added += 1
    return current_date

def calculate_days360(start_date, end_date):
    """Calculate days using 30/360 convention"""
    d1 = min(start_date.day, 30)
    d2 = min(end_date.day, 30) if d1 == 30 else end_date.day
    return 360 * (end_date.year - start_date.year) + \
           30 * (end_date.month - start_date.month) + \
           (d2 - d1)

def calculate_cashflow(amount, rate, days, convention):
    """Calculate cash flow based on daycount convention"""
    if convention == "A/365":
        return amount * rate * days / 365
    elif convention == "A/360":
        return amount * rate * days / 360
    else:  # 30/360
        return amount * rate * days / 360

def get_rate_index_value(rate_table, floating_ref=None, tenor_months=None, custodian=None, column='LAST_PRICE'):
    """Lookup value from rate index table with specific logic per field"""
    
    if column == 'LAST_PRICE' and floating_ref and not tenor_months:
        # ST Reference Rate: Match only on Floating Ref (C36 logic)
        mask = (rate_table['Floating Ref'] == floating_ref)
    elif column == 'LAST_PRICE' and tenor_months and not floating_ref:
        # Fixing Adjustment: Match only on Financing Tenor for LAST_PRICE (C37 logic)
        mask = (rate_table['M'] == tenor_months)
    elif column in ['Swap Cost', 'CoF v SOFR', 'Loan Spread'] and custodian and tenor_months:
        # Other costs: Match on both Custodian AND Financing Tenor (C38, C39, C40 logic)
        mask = (rate_table['Custodian'] == custodian) & (rate_table['M'] == tenor_months)
    else:
        # Fallback
        return 0.04
    
    result = rate_table[mask]
    if not result.empty:
        return result[column].iloc[0]
    return 0.04  # Default fallback

def generate_xirr_cashflows(equity, loan_notional, total_invested, interest_rate, coupon_rate,
                           start_date, end_date, interest_freq, coupon_freq):
    """Generate cash flows for XIRR calculation according to Complete_Net_Yield_Simulator_Requirements"""
    
    # Payment frequency mapping - months increment per payment
    freq_months = {
        "Quarterly": 3,
        "Semi-Annual": 6,
        "Annual": 12,
        "At Maturity": None  # Special case - only pays at end
    }
    
    interest_increment = freq_months[interest_freq]
    coupon_increment = freq_months[coupon_freq]
    
    # Generate separate date sequences for each payment type
    def generate_payment_dates(start_date, end_date, months_increment):
        """Generate payment dates based on frequency"""
        if months_increment is None:
            # "At Maturity" case - return empty list (payment only at end_date)
            return []
        
        dates = []
        current_date = start_date
        
        while True:
            current_date = start_date + relativedelta(months=len(dates) * months_increment + months_increment)
            if current_date >= end_date:
                break
            dates.append(current_date)
        
        return dates
    
    # Generate interest and coupon payment dates
    interest_dates = generate_payment_dates(start_date, end_date, interest_increment)
    coupon_dates = generate_payment_dates(start_date, end_date, coupon_increment)
    
    # Initialize cash flow arrays
    dates = [start_date]  # Start with initial investment date
    principal_flows = [-equity]  # Initial equity outflow
    interest_payments = [0]  # No interest at start
    coupon_receipts = [0]  # No coupon at start
    
    # Track the last interest and coupon payment dates separately
    last_interest_date = start_date
    last_coupon_date = start_date
    
    # Combine all unique dates and sort (excluding start_date, including end_date)
    all_payment_dates = set(interest_dates + coupon_dates + [end_date])
    sorted_dates = sorted(all_payment_dates)
    
    # Process each payment date
    for payment_date in sorted_dates:
        # Initialize cash flows for this date
        principal_flow = 0
        interest_payment = 0
        coupon_receipt = 0
        
        # Check if this is an interest payment date
        if payment_date in interest_dates or payment_date == end_date:
            # Calculate days since last interest payment
            interest_date_diff = (payment_date - last_interest_date).days
            # Interest Payment = -Loan_Drawn * Interest_Rate * (date_diff)/360
            interest_payment = -loan_notional * interest_rate * interest_date_diff / 360
            last_interest_date = payment_date
        
        # Check if this is a coupon payment date  
        if payment_date in coupon_dates or payment_date == end_date:
            # Calculate days since last coupon payment
            coupon_date_diff = (payment_date - last_coupon_date).days
            # Coupon Payment = Invested * Coupon_Rate * (date_diff)/360
            coupon_receipt = total_invested * coupon_rate * coupon_date_diff / 360
            last_coupon_date = payment_date
        
        # Principal return at maturity
        if payment_date == end_date:
            principal_flow = equity
        
        # Add this payment to the schedule
        dates.append(payment_date)
        principal_flows.append(principal_flow)
        interest_payments.append(interest_payment)
        coupon_receipts.append(coupon_receipt)
    
    # Calculate total cash flows (Column F = sum of C, D, E)
    total_cashflows = []
    for i in range(len(dates)):
        total_cashflows.append(principal_flows[i] + interest_payments[i] + coupon_receipts[i])
    
    return dates, principal_flows, interest_payments, coupon_receipts, total_cashflows

def calculate_xirr(dates, cashflows):
    """Calculate XIRR using proper Excel XIRR formula with fallback"""
    try:
        # Convert to numpy arrays
        dates_array = np.array(dates)
        cashflows_array = np.array(cashflows)
        
        # Check if we have enough data
        if len(cashflows_array) < 2 or len(dates_array) != len(cashflows_array):
            return 0.0
        
        # Convert dates to period numbers (days from start)
        start_date = dates_array[0]
        periods = [(d - start_date).days / 365.25 for d in dates_array]
        periods_array = np.array(periods)
        
        # XIRR calculation using Newton-Raphson method (Excel-compatible)
        def xirr_npv(rate):
            """Calculate NPV for given rate"""
            return sum([cf / ((1 + rate) ** period) for cf, period in zip(cashflows_array, periods_array)])
        
        def xirr_derivative(rate):
            """Calculate derivative of NPV function"""
            return sum([-period * cf / ((1 + rate) ** (period + 1)) 
                       for cf, period in zip(cashflows_array, periods_array)])
        
        # Newton-Raphson method for XIRR
        rate = 0.1  # Initial guess (10%)
        tolerance = 1e-8
        max_iterations = 100
        
        for iteration in range(max_iterations):
            npv = xirr_npv(rate)
            derivative = xirr_derivative(rate)
            
            # Check for convergence
            if abs(npv) < tolerance:
                break
                
            # Avoid division by zero
            if abs(derivative) < 1e-15:
                break
                
            # Newton-Raphson update
            rate_new = rate - npv / derivative
            
            # Check for convergence in rate
            if abs(rate_new - rate) < tolerance:
                break
                
            rate = rate_new
            
            # Prevent extreme values
            if rate > 10 or rate < -0.99:
                rate = 0.1  # Reset to initial guess
                break
        
        return rate
        
    except Exception as e:
        # Robust fallback calculation
        try:
            # Simple IRR approximation for fallback
            if len(cashflows) < 2:
                return 0.0
            
            # Basic approximation based on total return
            initial_investment = abs(cashflows[0])
            final_value = sum(cashflows[1:])
            
            if initial_investment > 0:
                total_return = final_value / initial_investment
                years = (dates[-1] - dates[0]).days / 365.25
                if years > 0:
                    return (total_return ** (1/years)) - 1
            
            return 0.0
        except:
            return 0.0

# Initialize session state
if 'calculated' not in st.session_state:
    st.session_state.calculated = False

# Load Rate Index Table
rate_index_table = load_rate_index_table()

# Sidebar Inputs (keeping configuration side the same)
with st.sidebar:
    st.markdown("<h3>Configuration</h3>", unsafe_allow_html=True)
    
    # Product Description
    st.markdown("<h4>Product Description</h4>", unsafe_allow_html=True)
    note_type = st.text_input("Note Type", value="TBC")
    underlying = st.text_input("Underlying Exposure", value="TBC")
    issuer = st.text_input("Issuer Name", value="TBC")

    st.divider()

    # Dates & Tenor
    st.markdown("<h4>Dates & Tenor</h4>", unsafe_allow_html=True)
    trade_date = st.date_input("Trade Date", value=datetime.today())
    days_to_settle = st.number_input("Days to Settle", value=5, min_value=1, max_value=30)
    
    # Calculate issue date
    issue_date_ts = calculate_workday(pd.to_datetime(trade_date), days_to_settle)
    issue_date = issue_date_ts.date() if hasattr(issue_date_ts, 'date') else issue_date_ts
    
    # Tenor input (manual)
    tenor_years = st.number_input(
        "Tenor (Years)", 
        value=3.0, 
        min_value=0.1, 
        max_value=10.0, 
        step=0.1, 
        format="%.1f"
    )
    
    # Calculate maturity date from tenor (not editable)
    maturity_date = issue_date_ts + relativedelta(months=int(tenor_years * 12)) - timedelta(days=1)
    
    # Display calculated values
    st.info(f"Issue Date: {issue_date.strftime('%Y-%m-%d')}")
    st.info(f"Maturity Date: {maturity_date.strftime('%Y-%m-%d')} (calculated)")
    
    # Calculate term values
    term_days = (maturity_date - issue_date_ts).days + 1
    term_months = round(((maturity_date.year - issue_date_ts.year) * 12 + 
                        (maturity_date.month - issue_date_ts.month)) + 
                       (maturity_date.day - issue_date_ts.day) / 30)
    term_years = round(term_days / 365.25, 2)

    st.info(f"Term: {term_days} days ({term_months} months, {term_years} years)")

    asset_daycount = st.selectbox("Asset Daycount Convention", ["30/360", "A/365", "A/360"])
    financing_tenor = st.number_input("Financing Tenor (Months)", value=12, min_value=1, max_value=60)
    liability_daycount = st.selectbox("Liability Daycount Convention", ["30/360", "A/365", "A/360"])
    
    st.divider()
    
    # XIRR Payment Frequency Controls (moved up)
    st.markdown("<h4>XIRR Payment Frequencies</h4>", unsafe_allow_html=True)
    interest_freq = st.selectbox(
        "Interest Payment Frequency", 
        ["Quarterly", "Semi-Annual", "Annual"], 
        index=0,
        key="interest_payment_freq_selector"
    )
    coupon_freq = st.selectbox(
        "Coupon Payment Frequency", 
        ["Annual", "Semi-Annual", "Quarterly", "At Maturity"], 
        index=0,
        key="coupon_payment_freq_selector"
    )
    
    st.divider()
    
    # Returns & Rates
    st.markdown("<h4>Returns & Rates</h4>", unsafe_allow_html=True)
    coupon_type = st.text_input("Coupon Type", value="Fixed")
    coupon_rate_pct = st.number_input(
        "Coupon Rate p.a. (%)", 
        min_value=0.0, 
        max_value=20.0, 
        value=5.0, 
        step=0.01, 
        format="%.2f"
    )
    coupon_rate = coupon_rate_pct / 100

    st.divider()

    # Funding Plan
    st.markdown("<h4>Funding Plan</h4>", unsafe_allow_html=True)
    equity = st.number_input("Equity (USD)", value=1500000, min_value=100000, step=100000)
    ltv_pct = st.number_input(
        "LTV (%)", 
        min_value=0.0, 
        max_value=95.0, 
        value=85.0, 
        step=0.1, 
        format="%.1f"
    )
    ltv = ltv_pct / 100
    loan_ratio = ltv / (1 - ltv) if ltv < 1 else 0
    total_invested = equity * (1 + loan_ratio)
    loan_notional = total_invested - equity

    st.info(f"Loan Ratio: {loan_ratio:.3f}")
    st.info(f"Total Invested: ${total_invested:,.0f}")
    st.info(f"Loan Notional: ${loan_notional:,.0f}")

    st.divider()

    # Borrowing Costs
    st.markdown("<h4>Borrowing Costs</h4>", unsafe_allow_html=True)
    lender = st.selectbox("Lender", ["CAI", "DB", "SG", "Barc"])
    floating_ref = st.selectbox("Floating Reference", ["1M", "3M", "6M", "12M"])

    # Calculate borrowing costs from rate index using correct logic
    st_reference_rate = get_rate_index_value(rate_index_table, floating_ref=floating_ref, column='LAST_PRICE')
    tenor_last_price = get_rate_index_value(rate_index_table, tenor_months=financing_tenor, column='LAST_PRICE')
    fixing_adjustment = tenor_last_price - st_reference_rate
    reference_rate = st_reference_rate + fixing_adjustment
    swap_cost = get_rate_index_value(rate_index_table, tenor_months=financing_tenor, custodian=lender, column='Swap Cost')
    cof_spread = get_rate_index_value(rate_index_table, tenor_months=financing_tenor, custodian=lender, column='CoF v SOFR')
    bank_spread = get_rate_index_value(rate_index_table, tenor_months=financing_tenor, custodian=lender, column='Loan Spread')
    total_borrowing_cost = reference_rate + swap_cost + cof_spread + bank_spread

    st.info(f"Total Borrowing Cost: {total_borrowing_cost:.3%}")

# Main Content Area - Three Tables Only
# Calculate cash flows
if asset_daycount == "A/365":
    coupon_cashflow = (total_invested * coupon_rate * term_days) / 365
elif asset_daycount == "A/360":
    coupon_cashflow = (total_invested * coupon_rate * term_days) / 360
else:  # 30/360
    days_360 = calculate_days360(issue_date_ts, maturity_date)
    coupon_cashflow = days_360 * coupon_rate * total_invested / 360

if liability_daycount == "A/365":
    borrowing_cost = (loan_notional * total_borrowing_cost * term_days) / 365
elif liability_daycount == "A/360":
    borrowing_cost = (loan_notional * total_borrowing_cost * term_days) / 360
else:  # 30/360
    days_360 = calculate_days360(issue_date_ts, maturity_date)
    borrowing_cost = days_360 * total_borrowing_cost * loan_notional / 360

net_yield_total = coupon_cashflow - borrowing_cost
net_yield_pa = net_yield_total / (equity * term_years) if term_years > 0 else 0

# Generate XIRR cash flows
dates, principal_flows, interest_payments, coupon_receipts, total_cashflows = generate_xirr_cashflows(
    equity, loan_notional, total_invested, total_borrowing_cost, 
    coupon_rate, issue_date_ts, maturity_date, interest_freq, coupon_freq
)

# Calculate XIRR
xirr_result = calculate_xirr(dates, total_cashflows)

# TABLE 1: Summary Table
st.markdown("### Summary", unsafe_allow_html=True)

# Create tenor display (e.g., "3Y")
tenor_display = f"{int(tenor_years)}Y" if tenor_years == int(tenor_years) else f"{tenor_years}Y"

summary_data = pd.DataFrame({
    'Parameter': [
        'Tenor',
        'Note Type',
        'Note Issuer',
        'Underlying / Reference Entity',
        'Drawn LTV (%)',
        'Coupon p.a. (%)',
        'Total Cost of Borrowing (%)',
        'Exp. Return on Equity p.a. (%)',
        'XIRR'
    ],
    'Value': [
        tenor_display,
        note_type,
        issuer,
        underlying,
        f"{ltv:.1%}",
        f"{coupon_rate:.2%}",
        f"{total_borrowing_cost:.3%}",
        f"{net_yield_pa:.2%}",
        f"{xirr_result:.2%}"
    ]
})

st.dataframe(summary_data, use_container_width=True, hide_index=True)

# TABLE 2: XIRR Table
st.markdown("### XIRR", unsafe_allow_html=True)

xirr_df = pd.DataFrame({
    'Date': dates,
    'Principal': principal_flows,
    'Interest': interest_payments,
    'Coupon': coupon_receipts,
    'Total Cash Flow': total_cashflows,
    'Cumulative': np.cumsum(total_cashflows)
})

st.dataframe(xirr_df.style.format({
    'Date': lambda x: x.strftime('%Y-%m-%d'),
    'Principal': '${:,.2f}',
    'Interest': '${:,.2f}',
    'Coupon': '${:,.2f}',
    'Total Cash Flow': '${:,.2f}',
    'Cumulative': '${:,.2f}'
}), use_container_width=True)

# TABLE 3: Rate Breakdown Table (moved from sidebar)
st.markdown("### Rate Breakdown", unsafe_allow_html=True)

rate_breakdown_data = pd.DataFrame({
    'Component': [
        'ST Reference Rate',
        'Fixing Adjustment', 
        'Reference Rate',
        'Swap Cost',
        'CoF v SOFR',
        'Bank Spread',
        'Total Cost of Borrowing'
    ],
    'Rate': [
        f"{st_reference_rate:.4%}",
        f"{fixing_adjustment:.4%}",
        f"{reference_rate:.4%}",
        f"{swap_cost:.4%}",
        f"{cof_spread:.4%}",
        f"{bank_spread:.4%}",
        f"{total_borrowing_cost:.4%}"
    ]
})

st.dataframe(rate_breakdown_data, use_container_width=True, hide_index=True)

# REVERSE CALCULATOR: Calculate Required Coupon Rate from Desired Net Yield
st.markdown("### Reverse Calculator", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    desired_net_yield_pct = st.number_input(
        "Desired Net Yield p.a. (%)",
        min_value=0.0,
        max_value=50.0,
        value=8.0,
        step=0.1,
        format="%.1f",
        help="Enter your target net yield to calculate the required coupon rate"
    )
    desired_net_yield = desired_net_yield_pct / 100

with col2:
    # Calculate required coupon rate
    # Net Yield = (Coupon - Borrowing Cost) / (Equity * Years)
    # Rearranging: Coupon = Net Yield * Equity * Years + Borrowing Cost
    # Required Coupon Rate = Coupon / Total Invested
    
    if term_years > 0:
        # Calculate required total coupon cash flow
        required_coupon_cashflow = (desired_net_yield * equity * term_years) + borrowing_cost
        
        # Calculate required coupon rate based on daycount convention
        if asset_daycount == "A/365":
            required_coupon_rate = (required_coupon_cashflow * 365) / (total_invested * term_days)
        elif asset_daycount == "A/360":
            required_coupon_rate = (required_coupon_cashflow * 360) / (total_invested * term_days)
        else:  # 30/360
            days_360_calc = calculate_days360(issue_date_ts, maturity_date)
            required_coupon_rate = (required_coupon_cashflow * 360) / (total_invested * days_360_calc)
        
        required_coupon_rate_pct = required_coupon_rate * 100
        
        # Display the result
        st.info(f"**Required Coupon Rate p.a.:** {required_coupon_rate_pct:.2f}%")
        
        # Show calculation details in an expander
        with st.expander("View Calculation Details"):
            st.write(f"To achieve a net yield of {desired_net_yield_pct:.1f}%:")
            st.write(f"- Total coupon income needed: ${required_coupon_cashflow:,.2f}")
            st.write(f"- Current borrowing cost: ${borrowing_cost:,.2f}")
            st.write(f"- Investment amount: ${total_invested:,.0f}")
            st.write(f"- Daycount convention: {asset_daycount}")
    else:
        st.warning("Cannot calculate - term years must be greater than 0")

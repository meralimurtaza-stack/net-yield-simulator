"""
Net Yield Simulator Pro - Fresh UI Version
Matching the screenshot design exactly
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
    st.warning("numpy-financial not available. Using fallback XIRR calculation.")

# Page Configuration
st.set_page_config(
    page_title="Net Yield Simulator Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"  # Can be "expanded" or "collapsed"
)

# ----------------------------------
# FRESH CSS - MATCHING SCREENSHOT
# ----------------------------------
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
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
    }
    
    section[data-testid="stSidebar"] > div {
        background-color: #e8ebf0 !important;
        padding-top: 2rem !important;
    }
    
    /* Enhanced collapse button styling */
    section[data-testid="stSidebar"] button[kind="header"] {
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        width: 40px !important;
        height: 40px !important;
        padding: 8px !important;
        margin: 0.5rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }
    
    section[data-testid="stSidebar"] button[kind="header"]:hover {
        background-color: #f9fafb !important;
        border-color: #5b6b89 !important;
        transform: translateX(2px) !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Collapsed sidebar styling */
    section[data-testid="stSidebar"][aria-expanded="false"] {
        min-width: 60px !important;
        max-width: 60px !important;
    }
    
    /* Show expand button when collapsed */
    button[data-testid="baseButton-header"] {
        background-color: #5b6b89 !important;
        border: none !important;
        border-radius: 0 8px 8px 0 !important;
        width: 48px !important;
        height: 48px !important;
        position: fixed !important;
        left: 0 !important;
        top: 1rem !important;
        z-index: 999 !important;
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.2s ease !important;
    }
    
    button[data-testid="baseButton-header"]:hover {
        background-color: #4a5a75 !important;
        transform: translateX(4px) !important;
        box-shadow: 4px 4px 12px rgba(0, 0, 0, 0.25) !important;
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
    
    section[data-testid="stSidebar"] input:focus,
    section[data-testid="stSidebar"] select:focus {
        border-color: #5b6b89 !important;
        box-shadow: 0 0 0 3px rgba(91, 107, 137, 0.1) !important;
        outline: none !important;
    }
    
    /* Sidebar Selectbox */
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 6px !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {
        background-color: #ffffff !important;
    }
    
    /* Remove inner borders and boxes from selectbox */
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div {
        border: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
    }
    
    /* Style the dropdown arrow properly */
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] svg {
        color: #4b5563 !important;
    }
    
    /* Clean selectbox text styling */
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] span {
        color: #1f2937 !important;
        font-size: 0.875rem !important;
    }
    
    /* Remove any lingering boxes */
    section[data-testid="stSidebar"] [role="button"] {
        background-color: transparent !important;
    }
    
    /* Sidebar Number Input Buttons */
    section[data-testid="stSidebar"] button[kind="secondary"] {
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
        color: #4b5563 !important;
    }
    
    section[data-testid="stSidebar"] button[kind="secondary"]:hover {
        background-color: #f9fafb !important;
        border-color: #5b6b89 !important;
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
    
    /* ==================== HEADER SECTION ==================== */
    .custom-header {
        background: linear-gradient(135deg, #5b6b89 0%, #4a5a75 100%);
        padding: 2.5rem 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .custom-header h1 {
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        letter-spacing: -0.5px;
    }
    
    .custom-header p {
        color: #d1d9e6 !important;
        font-size: 0.9375rem !important;
        margin: 0.5rem 0 0 0 !important;
        font-weight: 400 !important;
    }
    
    /* ==================== METRIC CARDS ==================== */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 1.25rem 1.5rem !important;
        border-radius: 10px !important;
        border: 1px solid #e5e7eb !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
    }
    
    div[data-testid="stMetric"] label {
        color: #6b7280 !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #111827 !important;
        font-size: 1.75rem !important;
        font-weight: 700 !important;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
        font-size: 0.8125rem !important;
        font-weight: 500 !important;
    }
    
    /* ==================== TABS ==================== */
    .stTabs {
        background-color: transparent !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background-color: transparent !important;
        border-bottom: none !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        color: #4b5563 !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f9fafb !important;
        border-color: #5b6b89 !important;
        color: #5b6b89 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #5b6b89 0%, #4a5a75 100%) !important;
        color: #ffffff !important;
        border-color: #5b6b89 !important;
    }
    
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }
    
    /* ==================== CONTENT SECTIONS ==================== */
    h3 {
        color: #111827 !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
        margin-top: 2rem !important;
    }
    
    h4 {
        color: #374151 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }
    
    /* ==================== INCOME/COST CARDS ==================== */
    .income-card {
        background: linear-gradient(135deg, #10b981 0%, #059669 50%, #047857 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
    }
    
    .cost-card {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 50%, #b91c1c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.25);
    }
    
    .income-card h4, .cost-card h4 {
        color: rgba(255, 255, 255, 0.9);
        margin: 0;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .income-card h2, .cost-card h2 {
        margin: 0.5rem 0 0.25rem 0;
        font-size: 1.75rem;
        font-weight: 700;
        color: white;
    }
    
    .income-card p, .cost-card p {
        margin: 0;
        opacity: 0.9;
        font-size: 0.8125rem;
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
    
    .streamlit-expanderHeader:hover {
        background-color: #f9fafb !important;
        border-color: #5b6b89 !important;
    }
    
    .streamlit-expanderContent {
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        padding: 1rem !important;
    }
    
    /* ==================== CHARTS ==================== */
    .js-plotly-plot {
        border-radius: 10px !important;
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        padding: 1rem !important;
    }
    
    /* ==================== RESULT HIGHLIGHT ==================== */
    .result-highlight {
        background: linear-gradient(135deg, #5b6b89 0%, #4a5a75 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 2rem 0;
        box-shadow: 0 4px 12px rgba(91, 107, 137, 0.3);
    }
    
    /* ==================== DIVIDERS ==================== */
    hr {
        margin: 2rem 0 !important;
        border: none !important;
        height: 1px !important;
        background-color: #e5e7eb !important;
    }
    
    /* ==================== BUTTONS ==================== */
    .stButton > button {
        background: linear-gradient(135deg, #5b6b89 0%, #4a5a75 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 4px 12px rgba(91, 107, 137, 0.3) !important;
        transform: translateY(-1px);
    }
    
    /* ==================== HIDE UNWANTED ELEMENTS ==================== */
    /* Only hide actual text nodes that say "keyboard_double_arrow" when icons fail to load */
    /* Do NOT hide the icon containers themselves */
    
    /* Fix for when Material Icons font fails - hide the fallback text */
    button[kind="header"] span:not(:has(svg)):not(:has(*)):empty::after,
    button[kind="header"] span:not(:has(svg)):not(:has(*)):empty::before {
        content: none !important;
    }
    
    /* Ensure icons display properly */
    button[kind="header"] svg,
    .streamlit-expanderHeader svg {
        display: inline-block !important;
        vertical-align: middle !important;
    }
    
    /* Hide only text that says "keyboard" specifically - not the icon containers */
    span:not(:has(svg)):not(:has(*)):only-child {
        font-size: 0 !important;
    }
    
    /* But ensure SVG icons are always visible */
    svg {
        font-size: 1.5rem !important;
    }

</style>
""", unsafe_allow_html=True)

# Real Rate Index Table Data from Excel (200 rows)
@st.cache_data  
def load_rate_index_table():
    """Load embedded rate index table data from Excel"""
    import pandas as pd
    
    # Real rate index data from your Excel file
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
        "Annual": 12
    }
    
    interest_increment = freq_months[interest_freq]
    coupon_increment = freq_months[coupon_freq]
    
    # Generate separate date sequences for each payment type
    def generate_payment_dates(start_date, end_date, months_increment):
        """Generate payment dates based on frequency"""
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

# Main Title Header
st.markdown("""
<div class="custom-header">
    <h1>Net Yield Simulator Pro</h1>
    <p>Professional Structured Product Calculator</p>
</div>
""", unsafe_allow_html=True)

# Load Rate Index Table
rate_index_table = load_rate_index_table()

# Sidebar Inputs
with st.sidebar:
    st.markdown("<h3>Configuration</h3>", unsafe_allow_html=True)
    

    # Product Description
    st.markdown("<h4>Product Description</h4>", unsafe_allow_html=True)
    note_type = st.selectbox("Note Type", ["CLN", "RCN", "DLN"])
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
    
    # Term (Months) - Complex ROUND formula with YEAR/MONTH functions
    term_months = round(((maturity_date.year - issue_date_ts.year) * 12 + 
                        (maturity_date.month - issue_date_ts.month)) + 
                       (maturity_date.day - issue_date_ts.day) / 30)
    
    # Term (Years) - ROUND(YEARFRAC(Issue_Date, Maturity_Date), 0)  
    term_years = round(term_days / 365.25, 2)  # More accurate year fraction

    st.info(f"Term: {term_days} days ({term_months} months, {term_years} years)")

    asset_daycount = st.selectbox("Asset Daycount Convention", ["30/360", "A/365", "A/360"])
    financing_tenor = st.number_input("Financing Tenor (Months)", value=12, min_value=1, max_value=60)
    liability_daycount = st.selectbox("Liability Daycount Convention", ["30/360", "A/365", "A/360"])
    
    st.divider()
    
    # Returns & Rates
    st.markdown("<h4>Returns & Rates</h4>", unsafe_allow_html=True)
    coupon_type = st.text_input("Coupon Type", value="Fixed")
    
    # Coupon Rate - manual input only
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

    # Funding Plan (C26-C30)
    st.markdown("<h4>Funding Plan</h4>", unsafe_allow_html=True)
    
    # C26: Equity (Input)
    equity = st.number_input("Equity (USD)", value=1500000, min_value=100000, step=100000)
    
    # C29: LTV (Input) - manual input only
    ltv_pct = st.number_input(
        "LTV (%)", 
        min_value=0.0, 
        max_value=95.0, 
        value=85.0, 
        step=0.1, 
        format="%.1f"
    )
    
    ltv = ltv_pct / 100
    
    # C30: Loan Ratio (Calculated) = LTV / (1 - LTV)
    loan_ratio = ltv / (1 - ltv) if ltv < 1 else 0
    
    # C28: Total Invested (Calculated) = Equity * (1 + Loan_Ratio)
    total_invested = equity * (1 + loan_ratio)
    
    # C27: Loan Notional (Calculated) = Total_Invested - Equity
    loan_notional = total_invested - equity

    # Display calculated values
    st.info(f"Loan Ratio: {loan_ratio:.3f}")
    st.info(f"Total Invested: ${total_invested:,.0f}")
    st.info(f"Loan Notional: ${loan_notional:,.0f}")

    st.divider()

    # Borrowing Costs
    st.markdown("<h4>Borrowing Costs</h4>", unsafe_allow_html=True)
    lender = st.selectbox("Lender", ["CAI", "DB", "SG", "Barc"])
    floating_ref = st.selectbox("Floating Reference", ["1M", "3M", "6M", "12M"])

    # Calculate borrowing costs from rate index using correct logic
    
    # C36: ST Reference Rate - Match only on Floating Ref
    st_reference_rate = get_rate_index_value(rate_index_table, floating_ref=floating_ref, column='LAST_PRICE')
    
    # C37: Fixing Adjustment - Match only on Financing Tenor, then subtract ST Rate
    tenor_last_price = get_rate_index_value(rate_index_table, tenor_months=financing_tenor, column='LAST_PRICE')
    fixing_adjustment = tenor_last_price - st_reference_rate
    
    # C35: Reference Rate = ST Reference Rate + Fixing Adjustment
    reference_rate = st_reference_rate + fixing_adjustment
    
    # C38: Swap Cost - Match on Lender AND Financing Tenor
    swap_cost = get_rate_index_value(rate_index_table, tenor_months=financing_tenor, custodian=lender, column='Swap Cost')
    
    # C39: CoF vs SOFR - Match on Lender AND Financing Tenor
    cof_spread = get_rate_index_value(rate_index_table, tenor_months=financing_tenor, custodian=lender, column='CoF v SOFR')
    
    # C40: Bank Spread - Match on Lender AND Financing Tenor
    bank_spread = get_rate_index_value(rate_index_table, tenor_months=financing_tenor, custodian=lender, column='Loan Spread')

    # C34: Total Cost of Borrowing = C35 + C38 + C39 + C40
    total_borrowing_cost = reference_rate + swap_cost + cof_spread + bank_spread

    # Display clean borrowing cost summary
    st.info(f"Total Borrowing Cost: {total_borrowing_cost:.3%}")
    
    # Optional detailed breakdown (collapsed by default)
    with st.expander("View Detailed Rate Breakdown"):
        rate_breakdown = pd.DataFrame({
            'Component': ['Reference Rate', 'ST Reference Rate', 'Fixing Adjustment', 'Swap Cost', 'CoF v SOFR', 'Bank Spread'],
            'Rate': [reference_rate, st_reference_rate, fixing_adjustment, swap_cost, cof_spread, bank_spread]
        })
        st.dataframe(rate_breakdown.style.format({'Rate': '{:.4%}'}), use_container_width=True)

# Main Content Area
col1, col2, col3, col4 = st.columns(4)

# Calculate cash flows using selected daycount conventions (C47-C54)
# Use the improved calculation method from tab1 for consistency
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

# C59: Net Yield (Total) = Selected_Coupon - Selected_Cost_of_Borrowing
net_yield_total = coupon_cashflow - borrowing_cost

# C60: Net Yield (p.a.) = Net_Yield_Total / (Equity * Term_Years)
net_yield_pa = net_yield_total / (equity * term_years) if term_years > 0 else 0

# Display Key Metrics (neutral delta colours)
with col1:
    st.metric("Net Yield p.a.", f"{net_yield_pa:.2%}", 
             delta=f"${net_yield_total:,.0f} total",
             delta_color="normal" if net_yield_pa > 0 else "inverse")

with col2:
    st.metric("Total Invested", f"${total_invested:,.0f}",
             delta=f"LTV: {ltv:.0%}")

with col3:
    st.metric("Loan Amount", f"${loan_notional:,.0f}",
             delta=f"Rate: {total_borrowing_cost:.2%}")

with col4:
    st.metric("Equity Amount", f"${equity:,.0f}",
             delta=f"{(1-ltv):.0%} of total")

# Detailed Analysis Tabs
tab1, tab2, tab3 = st.tabs(["Cash Flow Analysis", "XIRR Calculation", "Sensitivity Analysis"])

with tab1:
    st.markdown("<h3>Cash Flow Breakdown</h3>", unsafe_allow_html=True)

    # Calculate all daycount convention scenarios as per requirements
    conventions = ["A/365", "A/360", "30/360"]
    
    coupon_results = {}
    borrowing_results = {}
    net_results = {}
    
    for conv in conventions:
        if conv == "30/360":
            # C49 & C54: Use DAYS360 formula
            days_calc = calculate_days360(issue_date_ts, maturity_date)
        else:
            # C47, C48, C52, C53: Use actual term days
            days_calc = term_days
            
        # Coupon/Profit calculations (C47-C49)
        if conv == "A/365":
            # C47: (Total_Invested * Coupon_Rate * Term_Days) / 365
            coupon_cf = (total_invested * coupon_rate * term_days) / 365
        elif conv == "A/360": 
            # C48: (Total_Invested * Coupon_Rate * Term_Days) / 360
            coupon_cf = (total_invested * coupon_rate * term_days) / 360
        else:  # 30/360
            # C49: DAYS360(Issue_Date, Maturity_Date) * Coupon_Rate * Total_Invested / 360
            coupon_cf = days_calc * coupon_rate * total_invested / 360
            
        # Cost of Borrowing calculations (C52-C54)
        if conv == "A/365":
            # C52: (Loan_Notional * Total_Cost_of_Borrowing * Term_Days) / 365
            borrowing_cf = (loan_notional * total_borrowing_cost * term_days) / 365
        elif conv == "A/360":
            # C53: (Loan_Notional * Total_Cost_of_Borrowing * Term_Days) / 360
            borrowing_cf = (loan_notional * total_borrowing_cost * term_days) / 360
        else:  # 30/360
            # C54: DAYS360(Issue_Date, Maturity_Date) * Total_Cost_of_Borrowing * Loan_Notional / 360
            borrowing_cf = days_calc * total_borrowing_cost * loan_notional / 360
        
        net_cf = coupon_cf - borrowing_cf
        
        coupon_results[conv] = coupon_cf
        borrowing_results[conv] = borrowing_cf
        net_results[conv] = net_cf

    # Display selected convention results cleanly
    selected_coupon = coupon_results[asset_daycount]
    selected_borrowing = borrowing_results[liability_daycount]
    selected_net = selected_coupon - selected_borrowing
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class='income-card'>
            <h4>Coupon Income ({asset_daycount})</h4>
            <h2>${selected_coupon:,.2f}</h2>
            <p>Rate: {coupon_rate:.2%} on ${total_invested:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class='cost-card'>
            <h4>Borrowing Cost ({liability_daycount})</h4>
            <h2>${selected_borrowing:,.2f}</h2>
            <p>Rate: {total_borrowing_cost:.4%} on ${loan_notional:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)

    # Optional detailed analysis (collapsed by default)
    with st.expander("View All Daycount Convention Comparisons"):
        cf_data = pd.DataFrame({
            'Daycount Convention': conventions,
            'Coupon Income': [coupon_results[conv] for conv in conventions],
            'Borrowing Cost': [borrowing_results[conv] for conv in conventions],
            'Net Cash Flow': [net_results[conv] for conv in conventions],
            'Net Yield p.a.': [net_results[conv] / (equity * term_years) if term_years > 0 else 0 for conv in conventions]
        })

        st.dataframe(cf_data.style.format({
            'Coupon Income': '${:,.2f}',
            'Borrowing Cost': '${:,.2f}',
            'Net Cash Flow': '${:,.2f}',
            'Net Yield p.a.': '{:.2%}'
        }), use_container_width=True)

with tab2:
    st.markdown("<h3>XIRR Analysis</h3>", unsafe_allow_html=True)

    # Payment Frequency Controls - FIXED VERSION (no session state complications)
    c1, c2 = st.columns(2)
    with c1:
        interest_freq = st.selectbox(
            "Interest Payment Frequency", 
            ["Quarterly", "Semi-Annual", "Annual"], 
            index=0,
            key="interest_payment_freq_selector"
        )
        
    with c2:
        coupon_freq = st.selectbox(
            "Coupon Payment Frequency", 
            ["Annual", "Semi-Annual", "Quarterly"], 
            index=0,
            key="coupon_payment_freq_selector"
        )

    # Generate XIRR cash flows with fixed function
    dates, principal_flows, interest_payments, coupon_receipts, total_cashflows = generate_xirr_cashflows(
        equity, loan_notional, total_invested, total_borrowing_cost, 
        coupon_rate, issue_date_ts, maturity_date, interest_freq, coupon_freq
    )

    # Calculate XIRR using proper formula
    xirr_result = calculate_xirr(dates, total_cashflows)

    # Display XIRR result prominently
    st.markdown(f"""
    <div class="result-highlight">
        XIRR: {xirr_result:.2%}
    </div>
    """, unsafe_allow_html=True)

    # Payment Schedule Table
    st.markdown("<h4>Payment Schedule</h4>", unsafe_allow_html=True)

    schedule_df = pd.DataFrame({
        'Date': dates,
        'Principal': principal_flows,
        'Interest': interest_payments,
        'Coupon': coupon_receipts,
        'Total Cash Flow': total_cashflows,
        'Cumulative': np.cumsum(total_cashflows)
    })

    st.dataframe(schedule_df.style.format({
        'Date': lambda x: x.strftime('%Y-%m-%d'),
        'Principal': '${:,.2f}',
        'Interest': '${:,.2f}',
        'Coupon': '${:,.2f}',
        'Total Cash Flow': '${:,.2f}',
        'Cumulative': '${:,.2f}'
    }))

    # Visualize cash flows with better colors
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=dates,
        y=total_cashflows,
        name='Total Cash Flows',
        marker_color=['#dc3545' if cf < 0 else '#28a745' for cf in total_cashflows]
    ))

    fig.add_trace(go.Scatter(
        x=dates,
        y=np.cumsum(total_cashflows),
        name='Cumulative',
        mode='lines+markers',
        line=dict(color='#5b6b89', width=3),
        marker=dict(color='#5b6b89', size=8)
    ))

    fig.update_layout(
        title='Cash Flow Timeline (XIRR Analysis)',
        xaxis_title='Date',
        yaxis_title='Cash Flow ($)',
        hovermode='x unified',
        height=500,
        showlegend=True,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("<h3>Sensitivity Analysis</h3>", unsafe_allow_html=True)

    # Sensitivity to LTV
    ltv_range = np.arange(0.5, 0.95, 0.05)
    yields = []

    for ltv_test in ltv_range:
        loan_ratio_test = ltv_test / (1 - ltv_test)
        total_invested_test = equity * (1 + loan_ratio_test)
        loan_notional_test = total_invested_test - equity

        coupon_test = calculate_cashflow(total_invested_test, coupon_rate, days_calc, asset_daycount)
        cost_test = calculate_cashflow(loan_notional_test, total_borrowing_cost, days_calc, liability_daycount)

        net_yield_test = (coupon_test - cost_test) / (equity * term_years) if term_years > 0 else 0
        yields.append(net_yield_test)

    # Create sensitivity chart (line MAIN, vline MAIN dashed)
    fig_sens = go.Figure()

    fig_sens.add_trace(go.Scatter(
        x=ltv_range * 100,
        y=[y * 100 for y in yields],
        mode='lines+markers',
        name='Net Yield',
        line=dict(color='#5b6b89', width=3),
        marker=dict(color='#5b6b89')
    ))

    fig_sens.add_vline(x=ltv * 100, line_dash="dash", line_color='red', annotation_text=f"Current LTV: {ltv:.0%}", annotation_position="top left")

    fig_sens.update_layout(
        title='Net Yield Sensitivity to LTV',
        xaxis_title='LTV (%)',
        yaxis_title='Net Yield p.a. (%)',
        hovermode='x',
        height=400,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    st.plotly_chart(fig_sens, use_container_width=True)

    # Summary Statistics
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Min Yield", f"{min(yields):.2%}", delta=f"at {ltv_range[yields.index(min(yields))]:.0%} LTV", delta_color="off")
    with c2:
        st.metric("Max Yield", f"{max(yields):.2%}", delta=f"at {ltv_range[yields.index(max(yields))]:.0%} LTV", delta_color="off")
    with c3:
        st.metric("Current Yield", f"{net_yield_pa:.2%}", delta=f"at {ltv:.0%} LTV", delta_color="normal")

# Optional Technical Details (collapsed by default)
with st.expander("Technical Validation & Formula Details"):
    st.markdown("**Key Calculation Summary:**")
    
    summary_data = {
        'Component': ['Issue Date', 'Maturity Date', 'Term', 'Total Invested', 'Loan Notional', 'Borrowing Cost', 'Net Yield p.a.'],
        'Value': [
            issue_date_ts.strftime('%Y-%m-%d'),
            maturity_date.strftime('%Y-%m-%d'),
            f'{term_days} days ({term_years:.2f} years)',
            f'${total_invested:,.0f}',
            f'${loan_notional:,.0f}',
            f'{total_borrowing_cost:.3%}',
            f'{net_yield_pa:.2%}'
        ]
    }
    
    st.dataframe(pd.DataFrame(summary_data), use_container_width=True)
    
    # XIRR Summary
    st.markdown("**XIRR Calculation Summary:**")
    st.write(f"• Payment Frequencies: Interest {interest_freq}, Coupon {coupon_freq}")
    st.write(f"• XIRR Result: {xirr_result:.3%}")
    st.write("• Method: Newton-Raphson (Excel-compatible)")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 1.5rem;'>
    <p><strong>Net Yield Simulator Pro</strong></p>
    <p><em>Professional structured product calculator - for informational purposes only</em></p>
</div>
""", unsafe_allow_html=True)
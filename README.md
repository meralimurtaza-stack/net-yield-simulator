# Net Yield Simulator Pro

A professional financial calculator for structured products built with Streamlit.

## Features

- **Cash Flow Analysis**: Calculate coupon income and borrowing costs using multiple daycount conventions
- **XIRR Calculation**: Compute extended internal rate of return with customizable payment frequencies
- **Sensitivity Analysis**: Analyze net yield sensitivity to LTV ratios
- **Professional UI**: Clean, modern interface with responsive design

## Installation

### Local Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/net-yield-simulator.git
cd net-yield-simulator
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run net_yield_simulator_clean.py
```

### Streamlit Cloud Deployment

This app is deployed on Streamlit Cloud. Visit the live app at:
[Your App URL will appear here after deployment]

## Requirements

- Python 3.8+
- streamlit
- pandas
- numpy
- plotly
- python-dateutil
- xlsxwriter
- numpy-financial (optional, for enhanced XIRR calculation)

## Usage

1. Configure your product parameters in the sidebar:
   - Product Description (Note Type, Underlying, Issuer)
   - Dates & Tenor
   - Returns & Rates
   - Funding Plan
   - Borrowing Costs

2. View results across three tabs:
   - **Cash Flow Analysis**: See detailed income and cost breakdowns
   - **XIRR Calculation**: Analyze internal rate of return with payment schedules
   - **Sensitivity Analysis**: Explore yield sensitivity to different LTV ratios

## Configuration

The app uses an embedded rate index table for SOFR rates and borrowing costs. The table includes data for multiple custodians (DB, SG, Barc, CAI) across various tenors.

## License

This project is for internal use only.

## Author

Created for structured product analysis and net yield simulation.

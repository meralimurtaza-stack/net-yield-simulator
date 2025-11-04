# Net Yield Simulator - Complete Requirements Document

## Project Overview
Build a professional Net Yield Simulator web application using Python, Streamlit, and Claude Code that calculates yields for structured financial products (CLN, RCN, etc.). The application should be visually appealing, fully functional, and deployable as a shareable link.

---

# PART 1: Main Calculator (Rows 1-77)

## Section 1: Product Description
### Fields:
1. **Note Type** (C3)
   - Type: Input (Dropdown)
   - Options: CLN, RCN, DLN, etc.
   - Default: "CLN"
   - Description: Type of structured note being priced

2. **Underlying Exposure** (C4)
   - Type: Input (Text)
   - Default: "TBC"
   - Description: The underlying asset or reference entity

3. **Issuer Name** (C5)
   - Type: Input (Text)
   - Default: "TBC"
   - Description: Financial institution issuing the note

## Section 2: Tenor - Asset
### Fields:
4. **Trade Date** (C9)
   - Type: Input (Date Picker)
   - Default: Today's date
   - Formula: TODAY()
   - Description: Date when the trade is executed

5. **Days to Settle** (C10)
   - Type: Input (Integer)
   - Default: 5
   - Description: Business days between trade and settlement

6. **Issue Date** (C11)
   - Type: Calculated
   - Formula: WORKDAY(Trade_Date, Days_to_Settle)
   - Description: Settlement date (skips weekends)

7. **Maturity Date** (C12)
   - Type: Calculated
   - Formula: EDATE(Issue_Date, 36) - 1
   - Description: Final maturity date of the note

8. **Term (Days)** (C13)
   - Type: Calculated
   - Formula: (Maturity_Date - Issue_Date) + 1
   - Description: Total days from issue to maturity

9. **Term (Months)** (C14)
   - Type: Calculated
   - Formula: Complex ROUND formula with YEAR/MONTH functions
   - Description: Approximate months to maturity

10. **Term (Years)** (C15)
    - Type: Calculated
    - Formula: ROUND(YEARFRAC(Issue_Date, Maturity_Date), 0)
    - Description: Years to maturity (fractional)

11. **Asset Daycount Convention** (C16)
    - Type: Input (Dropdown)
    - Options: "30/360", "A/365", "A/360"
    - Default: "30/360"
    - Description: Day count convention for asset side

## Section 3: Tenor - Liability
### Fields:
12. **Financing Tenor (Months)** (C18)
    - Type: Input (Integer)
    - Default: 12
    - Description: Term of the financing facility

13. **Liability Daycount Convention** (C19)
    - Type: Input (Dropdown)
    - Options: "30/360", "A/365", "A/360"
    - Default: "30/360"
    - Description: Day count convention for liability side

## Section 4: Gross Return
### Fields:
14. **Coupon Type** (C22)
    - Type: Input (Dropdown)
    - Options: "Fixed", "Floating"
    - Default: "Fixed"
    - Description: Type of coupon payment

15. **Coupon Rate p.a.** (C23)
    - Type: Input (Percentage)
    - Default: 0.05 (5%)
    - Description: Annual coupon rate as decimal

## Section 5: Funding Plan
### Fields:
16. **Equity** (C26)
    - Type: Input (Integer)
    - Default: 1,500,000
    - Description: Amount of equity capital invested (USD)

17. **Loan Notional** (C27)
    - Type: Calculated
    - Formula: Total_Invested - Equity
    - Description: Amount borrowed/financed

18. **Total Invested** (C28)
    - Type: Calculated
    - Formula: Equity * (1 + Loan_Ratio)
    - Description: Total capital deployed (equity + loan)

19. **LTV** (C29)
    - Type: Input (Percentage)
    - Default: 0.85 (85%)
    - Description: Loan-to-Value ratio as decimal

20. **Loan Ratio** (C30)
    - Type: Calculated
    - Formula: LTV / (1 - LTV)
    - Description: Converts LTV to loan multiplier

## Section 6: Borrowing Cost
### Fields:
21. **Lender** (C33)
    - Type: Input (Dropdown)
    - Options: ["DB", "SG", "Barc", "CAI"]
    - Default: "CAI"
    - Description: Name of lending institution

22. **Total Cost of Borrowing** (C34)
    - Type: Calculated
    - Formula: Reference_Rate + Swap_Cost + CoF_vs_SOFR + Bank_Spread
    - Description: All-in borrowing cost p.a.

23. **Reference Rate** (C35)
    - Type: Calculated
    - Formula: ST_Reference_Rate + Fixing_Adjustment
    - Description: Base reference rate

24. **Floating Ref** (D37)
    - Type: Input (Dropdown)
    - Options: ["1M", "3M", "6M", "12M"]
    - Default: "3M"
    - Description: Floating reference period

25. **ST Reference Rate** (C36)
    - Type: Calculated (Lookup from Rate Index Table)
    - Formula: LOOKUP(Floating_Ref in Rate_Index_Table)
    - Description: Short-term reference rate from Rate Index

26. **Fixing Adjustment** (C37)
    - Type: Calculated (Lookup from Rate Index Table)
    - Formula: LOOKUP(Financing_Tenor in Rate_Index_Table) - ST_Reference_Rate
    - Description: Historical adjustment to reference rate

27. **Swap Cost** (C38)
    - Type: Calculated (Lookup from Rate Index Table)
    - Formula: LOOKUP(Lender, Financing_Tenor in Rate_Index_Table)
    - Description: Cost of interest rate swap

28. **CoF vs SOFR** (C39)
    - Type: Calculated (Lookup from Rate Index Table)
    - Formula: LOOKUP(Lender, Financing_Tenor in Rate_Index_Table)
    - Description: Cost of Funds vs SOFR spread

29. **Bank Spread** (C40)
    - Type: Calculated (Lookup from Rate Index Table)
    - Formula: LOOKUP(Lender, Financing_Tenor in Rate_Index_Table)
    - Description: Bank's lending spread

## Section 7: Cash Flow Calculations
### Coupon/Profit Calculations:
30. **Coupon/Profit (A/365)** (C47)
    - Formula: (Total_Invested * Coupon_Rate * Term_Days) / 365

31. **Coupon/Profit (A/360)** (C48)
    - Formula: (Total_Invested * Coupon_Rate * Term_Days) / 360

32. **Coupon/Profit (30/360)** (C49)
    - Formula: DAYS360(Issue_Date, Maturity_Date) * Coupon_Rate * Total_Invested / 360

### Cost of Borrowing Calculations:
33. **Cost of Borrowing (A/365)** (C52)
    - Formula: (Loan_Notional * Total_Cost_of_Borrowing * Term_Days) / 365

34. **Cost of Borrowing (A/360)** (C53)
    - Formula: (Loan_Notional * Total_Cost_of_Borrowing * Term_Days) / 360

35. **Cost of Borrowing (30/360)** (C54)
    - Formula: DAYS360(Issue_Date, Maturity_Date) * Total_Cost_of_Borrowing * Loan_Notional / 360

## Section 8: Net Return
### Fields:
36. **Net Yield (Total)** (C59)
    - Type: Calculated
    - Formula: Selected_Coupon - Selected_Cost_of_Borrowing
    - Description: Total net return over investment period

37. **Net Yield (p.a.)** (C60)
    - Type: Output (KEY RESULT)
    - Formula: Net_Yield_Total / (Equity * Term_Years)
    - Description: Annual percentage return on equity

## Section 9: Output Summary
All output fields that summarize the calculation for display:
- Report Title (concatenation of term, type, underlying)
- All key metrics for display

---

# PART 2: XIRR Calculations (Row 78 onwards)

## XIRR Calculation Section

### Payment Frequency Controls (NEW FEATURES):
1. **Interest Payment Frequency**
   - Type: Dropdown
   - Options: ["Quarterly", "Semi-Annual", "Annual"]
   - Default: "Quarterly"
   - Location: Suggested G75

2. **Coupon Payment Frequency**
   - Type: Dropdown
   - Options: ["Quarterly", "Semi-Annual", "Annual"]
   - Default: "Annual"
   - Location: Suggested G76

### Cash Flow Grid (B80:F101):
- **Column B**: Dates (dynamic based on frequencies)
- **Column C**: Principal flows (-initial, +final)
- **Column D**: Interest payments (negative, based on frequency)
- **Column E**: Coupon receipts (positive, based on frequency)
- **Column F**: Total cash flow (sum of C, D, E)

### Key Formulas:
- **Interest Payment**: = -Loan_Drawn * Interest_Rate * (date_diff)/360
- **Coupon Payment**: = Invested * Coupon_Rate * (date_diff)/360
- **XIRR**: = XIRR(Cash_Flow_Column, Date_Column)

### Dynamic Date Generation:
```python
def generate_payment_dates(start_date, frequency, term_years):
    if frequency == "Quarterly":
        months_increment = 3
    elif frequency == "Semi-Annual":
        months_increment = 6
    else:  # Annual
        months_increment = 12
    
    dates = [start_date]
    current_date = start_date
    end_date = start_date + timedelta(days=term_years*365)
    
    while current_date < end_date:
        current_date = add_months(current_date, months_increment)
        dates.append(min(current_date, end_date))
    
    return dates
```

---

# EMBEDDED RATE INDEX TABLE

## Rate Index Table Structure
The following data should be embedded in the application code as a pandas DataFrame:

```python
RATE_INDEX_DATA = {
    'Ticker1': ['USOSFR1Z', 'USOSFR2Z', 'USOSFR3Z', ...],
    'Floating Ref': ['1M', '2M', '3M', ...],
    'M': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],  # Months
    'LAST_PRICE': [0.038876, 0.039076, 0.038875, ...],  # Reference rates
    'Custodian': ['DB', 'SG', 'Barc', 'CAI', ...],
    'CoF v SOFR': [0.0020, 0.0025, 0.0030, ...],
    'Swap Cost': [0.0003, 0.0003, 0.0004, ...],
    'Loan Spread': [0.0045, 0.0050, 0.0055, ...]
}
```

## Lookup Functions Required:
1. **get_reference_rate(floating_ref)**: Returns LAST_PRICE for matching Floating Ref
2. **get_fixing_adjustment(tenor_months, st_rate)**: Returns rate for tenor minus ST rate
3. **get_swap_cost(lender, tenor_months)**: Returns Swap Cost for lender/tenor combo
4. **get_cof_spread(lender, tenor_months)**: Returns CoF v SOFR for lender/tenor
5. **get_bank_spread(lender, tenor_months)**: Returns Loan Spread for lender/tenor

---

# UI/UX Requirements

## Design Principles:
1. **Modern, Professional Interface**
   - Clean, card-based layout
   - Gradient backgrounds for key metrics
   - Smooth animations and transitions
   - Responsive design

2. **Color Scheme**:
   - Primary: Purple gradient (#667eea to #764ba2)
   - Secondary: Light grays and whites
   - Success: Green for positive yields
   - Warning: Orange for caution metrics

3. **Layout Structure**:
   - Header with application title
   - Input sections in collapsible cards
   - Real-time calculation updates
   - Prominent display of Net Yield result
   - XIRR section with payment schedule visualization

4. **Interactive Elements**:
   - Date pickers for date inputs
   - Dropdown menus for selections
   - Sliders for percentages
   - Toggle switches for daycount conventions
   - Export functionality for results

## Key Features:
1. **Real-time Calculations**: All calculated fields update automatically
2. **Data Validation**: Input validation with appropriate error messages
3. **Export Options**: Download results as PDF or Excel
4. **Responsive Design**: Works on desktop and tablet
5. **Help Tooltips**: Contextual help for complex fields

---

# Technical Implementation Notes

## Technology Stack:
- **Backend**: Python 3.8+
- **Framework**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Date Handling**: datetime, dateutil
- **Financial Calculations**: numpy-financial (for XIRR)
- **Export**: xlsxwriter, reportlab

## Key Python Libraries:
```python
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import numpy_financial as npf
```

## Deployment:
- Use Streamlit Cloud for hosting
- Environment variables for any sensitive data
- Session state for maintaining user inputs
- Caching for performance optimization

---

# Testing Requirements

## Functional Tests:
1. Verify all formulas match Excel calculations
2. Test all dropdown and input combinations
3. Validate XIRR calculations for different payment frequencies
4. Ensure proper date handling including weekends/holidays
5. Test edge cases (0% rates, 100% LTV, etc.)

## User Acceptance Criteria:
1. Results match existing Excel calculator within 0.01%
2. Page loads in under 2 seconds
3. All calculations update in real-time
4. Export functions work correctly
5. UI is intuitive without training

---

# Version Control & Documentation
- Version 1.0: Initial release with core functionality
- Include inline code documentation
- User guide with examples
- Technical documentation for maintenance

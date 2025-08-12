
# Amortization Table Generator

## Overview
This project provides a Python script that calculates an amortization schedule for a loan, given:
1. **Principal amount**
2. **Annual interest rate**
3. **Amortization term** (in years)
4. **Maturity term** (in years)

It supports loans with balloon payments by allowing the maturity term to be shorter than the amortization term.

## Features
- **PMT Calculation**: Uses the standard payment formula to calculate fixed periodic payments.
- **Amortization Schedule**: Outputs each period's payment, interest portion, principal portion, remaining balance, and balloon payment (if applicable).
- **Balloon Payment Handling**: If the loan matures before being fully amortized, the remaining balance is displayed as a balloon due at maturity.
- **Configurable Payments-per-Year**: Defaults to monthly payments (12/year).

## Example (from our discussion)
- **Principal**: 200,000
- **Interest rate**: 5.4% annually
- **Amortization**: 240 months (20 years)
- **Maturity**: 60 months (5 years, balloon at maturity)

### Results
- **Monthly Payment**: 1,364.50
- **Total Interest Paid to Month 60**: 49,956.60
- **Balloon Due at Month 60**: 168,086.43

## Usage
Run the script directly to print an amortization table for the example scenario:

```bash
python amortization.py
```

Modify the `principal`, `annual_rate`, `amort_months`, and `maturity_months` variables in the `__main__` section to suit your needs.

## Output
The output table contains:
- **payment**: Total payment amount for the period
- **interest**: Portion of the payment that goes toward interest
- **principal**: Portion of the payment that goes toward reducing principal
- **balance_end**: Remaining balance after the payment
- **balloon_due**: Remaining balance due at maturity (only shown in the final row if applicable)

## Streamlit App

This repo also contains a Streamlit app for interactive use.

### Quickstart

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app**
   ```bash
   streamlit run streamlit_app.py
   ```

3. Open the local URL that Streamlit prints (usually `http://localhost:8501`),
   then set:
   - **Principal**
   - **Annual Interest Rate (%)**
   - **Amortization (months)**
   - **Maturity (months)**

The app will compute:
- Fixed periodic payment from the amortization term
- Full table up to maturity (showing any **balloon due** on the last row)
- Summary metrics and a balance-over-time chart
- A CSV download of the table


## Interest Rate Interpolator (PCHIP)

This repo includes a PCHIP-based interest rate interpolator that takes sparse (period, rate) points and fills the curve without overshoot.

- Core module: `rate_interpolator.py`
- Streamlit page: `pages/02_Rate_Interpolator.py`

Run the multi-page app:
    streamlit run streamlit_app.py
Then open "Interest Rate Interpolator (PCHIP)" from the sidebar.

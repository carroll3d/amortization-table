
import streamlit as st
import pandas as pd
from dataclasses import dataclass, asdict
from math import isclose

# ---------------- Functions ----------------

@dataclass
class AmortRow:
    period: int
    payment: float
    interest: float
    principal: float
    balance_end: float
    balloon_due: float = 0.0

def pmt(principal: float, annual_rate: float, amort_years: float, payments_per_year: int = 12) -> float:
    n = int(round(amort_years * payments_per_year))
    if n <= 0:
        raise ValueError("Amortization term must be > 0.")
    if isclose(annual_rate, 0.0, abs_tol=1e-15):
        return principal / n
    r = annual_rate / payments_per_year
    return principal * r / (1 - (1 + r) ** (-n))

def amortization_schedule(
    principal: float,
    annual_rate: float,
    amort_years: float,
    maturity_years: float,
    payments_per_year: int = 12,
    round_to_cents: bool = True
):
    if principal <= 0:
        raise ValueError("Principal must be > 0.")
    if maturity_years <= 0:
        raise ValueError("Maturity term must be > 0.")
    r = annual_rate / payments_per_year
    pay = pmt(principal, annual_rate, amort_years, payments_per_year)
    periods_to_list = int(round(maturity_years * payments_per_year))
    schedule = []
    bal = float(principal)
    for k in range(1, periods_to_list + 1):
        interest = bal * r
        principal_pay = pay - interest
        if principal_pay > bal:
            principal_pay = bal
            pay_effective = interest + principal_pay
        else:
            pay_effective = pay
        bal = bal - principal_pay
        if round_to_cents:
            interest = round(interest, 2)
            principal_pay = round(principal_pay, 2)
            pay_effective = round(pay_effective, 2)
            bal = round(bal, 2)
        schedule.append(AmortRow(
            period=k,
            payment=pay_effective,
            interest=interest,
            principal=principal_pay,
            balance_end=bal,
            balloon_due=0.0
        ))
        if bal <= 0.0:
            break
    if len(schedule) == periods_to_list and schedule[-1].balance_end > 0:
        last = schedule[-1]
        schedule[-1] = AmortRow(
            period=last.period,
            payment=last.payment,
            interest=last.interest,
            principal=last.principal,
            balance_end=last.balance_end,
            balloon_due=last.balance_end
        )
    return schedule

# ---------------- Streamlit UI ----------------

st.title("Amortization Table Generator with Balloon Payment Option")

# Inputs
principal = st.number_input("Principal Amount", value=200000.0, min_value=0.0, step=1000.0)
annual_rate_percent = st.number_input("Annual Interest Rate (%)", value=5.4, min_value=0.0, step=0.1)
amort_months = st.number_input("Amortization Term (months)", value=240, min_value=1, step=1)
maturity_months = st.number_input("Maturity Term (months)", value=60, min_value=1, step=1)
payments_per_year = st.selectbox("Payments per Year", options=[12, 4, 2, 1], index=0)

# Calculate button
if st.button("Generate Amortization Table"):
    amort_years = amort_months / 12
    maturity_years = maturity_months / 12
    sched = amortization_schedule(
        principal, annual_rate_percent / 100, amort_years, maturity_years,
        payments_per_year=payments_per_year, round_to_cents=True
    )
    df = pd.DataFrame([asdict(r) for r in sched])
    df.index = df['period']
    df_display = df[['payment','interest','principal','balance_end','balloon_due']]
    
    st.subheader("Amortization Table")
    st.dataframe(df_display)
    
    # Summary
    total_interest = df['interest'].sum()
    monthly_payment = df['payment'].iloc[0]
    balloon_due = df['balloon_due'].iloc[-1]
    st.write(f"**Periodic Payment:** {monthly_payment:,.2f}")
    st.write(f"**Total Interest Paid to Maturity:** {total_interest:,.2f}")
    st.write(f"**Balloon Payment at Maturity:** {balloon_due:,.2f}")
    
    # CSV Download
    csv = df_display.to_csv(index_label="period").encode('utf-8')
    st.download_button(label="Download CSV", data=csv, file_name="amortization_table.csv", mime="text/csv")

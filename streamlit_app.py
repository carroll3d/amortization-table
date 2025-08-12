import streamlit as st
import pandas as pd
from dataclasses import asdict
from amortization_core import amortization_schedule, pmt

st.set_page_config(page_title="Amortization Table with Balloon", page_icon="💸", layout="wide")

st.title("💸 Amortization Table Generator (Balloon Loans Supported)")

with st.sidebar:
    st.header("Loan Inputs")
    colA, colB = st.columns(2)
    with colA:
        principal = st.number_input("Principal", value=200_000.00, step=1000.0, min_value=0.0, format="%.2f")
        rate_pct = st.number_input("Annual Interest Rate (%)", value=5.40, step=0.01, min_value=0.0, format="%.2f")
    with colB:
        amort_months = st.number_input("Amortization (months)", value=240, step=1, min_value=1)
        maturity_months = st.number_input("Maturity (months)", value=60, step=1, min_value=1)

    payments_per_year = st.selectbox("Payments per year", options=[12, 24, 26, 52], index=0, help="12=monthly, 24=semi-monthly, 26=biweekly, 52=weekly")
    round_to_cents = st.checkbox("Round to cents", value=True)

    st.markdown("---")
    st.caption("Tip: Set maturity < amortization to model a balloon at maturity.")

# Compute schedule
amort_years = amort_months / 12
maturity_years = maturity_months / 12
annual_rate = rate_pct / 100.0

pay = pmt(principal, annual_rate, amort_years, payments_per_year)
schedule = amortization_schedule(
    principal=principal,
    annual_rate=annual_rate,
    amort_years=amort_years,
    maturity_years=maturity_years,
    payments_per_year=payments_per_year,
    round_to_cents=round_to_cents
)

df = pd.DataFrame([asdict(r) for r in schedule]).set_index("period")

# Summary metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("Payment", f"${pay:,.2f}")
total_interest = df["interest"].sum()
c2.metric("Interest to Maturity", f"${total_interest:,.2f}")
balloon = df["balloon_due"].iloc[-1] if "balloon_due" in df.columns else 0.0
c3.metric("Balloon at Maturity", f"${balloon:,.2f}")
c4.metric("Periods Listed", f"{len(df):,}")

st.markdown("### Amortization Table")
st.dataframe(df[["payment","interest","principal","balance_end","balloon_due"]], use_container_width=True, height=480)

# Chart
st.markdown("### Balance Over Time")
st.line_chart(df["balance_end"])

# Download CSV
csv = df.to_csv(index=True).encode("utf-8")
st.download_button("Download CSV", data=csv, file_name="amortization_schedule.csv", mime="text/csv")

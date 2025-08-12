import streamlit as st
import numpy as np
import pandas as pd
from rate_interpolator import make_curve, interpolate_range

st.set_page_config(page_title="Rate Interpolator (PCHIP)", page_icon="📈", layout="wide")
st.title("📈 Interest Rate Interpolator (PCHIP)")

st.markdown("""
Provide known **(period, rate)** points, then interpolate missing periods using a
**shape-preserving PCHIP** curve. Rates can be **percent** (5.4) or **decimal** (0.054).
""")

with st.sidebar:
    st.header("Known Points")
    demo = st.checkbox("Load demo data", value=True)
    if demo:
        df_known = pd.DataFrame({"period":[0,6,12,24,36,60], "rate":[5.0,5.2,5.4,5.8,6.0,6.3]})
    else:
        df_known = pd.DataFrame({"period":[0,12], "rate":[5.0,6.0]})
    df_known = st.data_editor(df_known, num_rows="dynamic", use_container_width=True)

    st.markdown("---")
    st.header("Query Range")
    c1,c2,c3 = st.columns(3)
    with c1:
        q_start = st.number_input("Start period", value=float(0), step=1.0)
    with c2:
        q_end = st.number_input("End period", value=float(60), step=1.0)
    with c3:
        q_step = st.number_input("Step", value=float(1), min_value=0.0001, step=1.0)

try:
    curve = make_curve(df_known["period"].values, df_known["rate"].values)
    qx, qy = interpolate_range(curve, start=q_start, end=q_end, step=q_step)
    df_out = pd.DataFrame({"period":qx, "rate_decimal":qy, "rate_percent":qy*100.0})

    st.success("Interpolation successful.")
    c1, c2 = st.columns([2,1])
    with c1:
        st.markdown("### Interpolated Curve")
        st.line_chart(df_out.set_index("period")[["rate_decimal"]])
    with c2:
        st.markdown("### Table")
        st.dataframe(df_out, use_container_width=True, height=520)

    csv = df_out.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", data=csv, file_name="interpolated_rates.csv", mime="text/csv")

except Exception as e:
    st.error(f"{e}")

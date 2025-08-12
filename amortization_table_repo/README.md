
## Interest Rate Interpolator (PCHIP)

This repo also includes a **PCHIP-based interest rate interpolator** that takes sparse (period, rate) points and fills the curve without overshoot.

- Core module: `rate_interpolator.py`
- Streamlit page: `pages/02_Rate_Interpolator.py`

**Run the multi-page app**
```bash
streamlit run streamlit_app.py
```
Then open **"Interest Rate Interpolator (PCHIP)"** from the sidebar.

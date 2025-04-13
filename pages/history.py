import streamlit as st
import pandas as pd

st.title("📜 Loan History")

if "history" in st.session_state and len(st.session_state["history"]) > 0:
    history_df = pd.DataFrame(st.session_state["history"])
    st.dataframe(history_df.style.format("₹{:,.0f}"))
else:
    st.info("No history available yet. Run a calculation and click 'Save'.")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="DebtSync", layout="centered")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Title
st.title("🏠 DebtSync [Loan Repayment Calculator]")

# Input Section
st.write("### 📥 Enter Loan Details (All values in ₹)")

col1, col2 = st.columns(2)
home_value = col1.number_input("Home Value (₹)", min_value=0, value=5000000)
deposit = col1.number_input("Deposit (₹)", min_value=0, value=1000000)
interest_rate = col2.number_input("Interest Rate (%)", min_value=0.0, value=7.5)
loan_term = col2.number_input("Loan Term (Years)", min_value=1, value=20)

# Loan calculation
loan_amount = home_value - deposit
monthly_interest_rate = (interest_rate / 100) / 12
number_of_payments = loan_term * 12

monthly_payment = (
    loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
    / ((1 + monthly_interest_rate) ** number_of_payments - 1)
)

total_payments = monthly_payment * number_of_payments
total_interest = total_payments - loan_amount

# Display Metrics
st.write("### 💸 Loan Repayment Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Monthly EMI", f"₹{monthly_payment:,.2f}")
col2.metric("Total Repayment", f"₹{total_payments:,.0f}")
col3.metric("Total Interest", f"₹{total_interest:,.0f}")

# Generate Schedule
schedule = []
remaining_balance = loan_amount
for i in range(1, number_of_payments + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i / 12)
    schedule.append([i, monthly_payment, principal_payment, interest_payment, remaining_balance, year])

df = pd.DataFrame(schedule, columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"])

# Line Chart
st.write("### 📈 Yearly Loan Balance Trend")
payments_df = df.groupby("Year")[["Remaining Balance"]].min()
st.line_chart(payments_df)

# Save to session state
if "history" not in st.session_state:
    st.session_state["history"] = []

if st.button("💾 Save This Calculation to History"):
    st.session_state["history"].append({
        "Home Value (₹)": home_value,
        "Deposit (₹)": deposit,
        "Loan Amount (₹)": loan_amount,
        "Monthly EMI": monthly_payment,
        "Total Interest (₹)": total_interest,
        "Total Repayment (₹)": total_payments
    })
    st.success("✅ Calculation saved to history!")

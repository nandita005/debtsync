import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

st.set_page_config(page_title="📊 Visualizations", layout="centered")

st.title("📊 Loan Visualization Charts")

# Apply custom CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Check for saved history
if "history" not in st.session_state or len(st.session_state["history"]) == 0:
    st.warning("No history available. Please calculate and save a loan from the home page.")
    st.stop()

# Get latest saved loan
latest = st.session_state["history"][-1]

# Display latest data
st.write("### 📌 Latest Loan Summary")
st.json(latest)

# Pie Chart: Loan Amount vs Interest
st.write("### 🥧 Loan vs Interest Distribution")
fig1, ax1 = plt.subplots()
sizes = [latest["Loan Amount (₹)"], latest["Total Interest (₹)"]]
labels = ["Principal Loan", "Total Interest"]
colors = ["#1f77b4", "#ff7f0e"]
ax1.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
ax1.axis("equal")
st.pyplot(fig1)

# Bar Chart: EMI, Interest, Total Repayment
st.write("### 📊 Loan Components")
components = {
    "Monthly EMI": latest["Monthly EMI"],
    "Total Interest (₹)": latest["Total Interest (₹)"],
    "Total Repayment (₹)": latest["Total Repayment (₹)"]
}
fig2, ax2 = plt.subplots()
bars = ax2.bar(components.keys(), components.values(), color=["#4CAF50", "#FF9800", "#2196F3"])
ax2.set_ylabel("Amount (₹)")
ax2.set_title("Loan Breakdown")
st.pyplot(fig2)

# Scatter Plot: Loan vs EMI
st.write("### 📈 Loan Amount vs Monthly EMI")
df = pd.DataFrame(st.session_state["history"])
fig3, ax3 = plt.subplots()
sns.scatterplot(data=df, x="Loan Amount (₹)", y="Monthly EMI", ax=ax3, color="purple", s=100)
ax3.set_title("Loan vs EMI Trend")
st.pyplot(fig3)

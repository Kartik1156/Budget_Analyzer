import streamlit as st
import matplotlib.pyplot as plt

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Budget Analyzer", layout="wide")

# -------------------------
# LIGHT UI IMPROVEMENT (Minimal & Clean)
# -------------------------
st.markdown("""
<style>
h1 {
    color: #2E7D32;
}
.stButton>button {
    border-radius: 8px;
    padding: 8px 16px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------
st.title("💸 Smart Budget Risk Analyzer")
st.write("Analyze your spending and financial risk")

# -------------------------
# INPUT SECTION
# -------------------------
col1, col2 = st.columns(2)

with col1:
    income = st.number_input("💰 Monthly Income (₹)", min_value=1)

with col2:
    growth = st.slider("📈 Expected Expense Growth (%)", 0, 50, 10)

st.markdown("### 🧾 Monthly Expenses")

colA, colB, colC = st.columns(3)

with colA:
    food = st.number_input("Food", min_value=0)
    travel = st.number_input("Travel", min_value=0)

with colB:
    rent = st.number_input("Rent", min_value=0)
    shopping = st.number_input("Shopping", min_value=0)

with colC:
    entertainment = st.number_input("Entertainment", min_value=0)
    other = st.number_input("Other", min_value=0)

# -------------------------
# CALCULATIONS
# -------------------------
total_expense = food + rent + travel + shopping + entertainment + other
savings = income - total_expense

expense_ratio = total_expense / income if income else 0
savings_ratio = savings / income if income else 0

future_expense = total_expense * (1 + growth / 100)
future_savings = income - future_expense

risk_score = min(max(expense_ratio, 0), 1)

# -------------------------
# BUTTON
# -------------------------
if st.button("📊 Analyze Budget"):

    st.markdown("## 📊 Results")

    colX, colY = st.columns(2)

    # -------------------------
    # METRICS
    # -------------------------
    with colX:
        st.metric("Total Expense", f"₹{total_expense}")
        st.metric("Savings", f"₹{savings}")
        st.metric("Savings %", f"{savings_ratio*100:.1f}%")

        st.subheader("Risk Level")
        st.progress(int(risk_score * 100))

        if risk_score > 0.9:
            st.error("🚨 Very High Risk")
        elif risk_score > 0.7:
            st.warning("⚠️ High Risk")
        elif risk_score > 0.5:
            st.warning("⚠️ Moderate Risk")
        else:
            st.success("✅ Low Risk")

    # -------------------------
    # PIE CHART
    # -------------------------
    with colY:
        labels = ["Food", "Rent", "Travel", "Shopping", "Entertainment", "Other"]
        values = [food, rent, travel, shopping, entertainment, other]

        fig1, ax1 = plt.subplots()
        ax1.pie(values, labels=labels, autopct='%1.1f%%')
        ax1.set_title("Expense Distribution")

        st.pyplot(fig1)

    # -------------------------
    # BAR GRAPH
    # -------------------------
    st.subheader("📊 Category-wise Spending")

    categories = ["Food", "Rent", "Travel", "Shopping", "Entertainment", "Other"]
    values = [food, rent, travel, shopping, entertainment, other]

    fig2, ax2 = plt.subplots()
    ax2.bar(categories, values)
    ax2.set_title("Spending Comparison")

    st.pyplot(fig2)

    # -------------------------
    # FUTURE ANALYSIS
    # -------------------------
    st.subheader("🔮 Future Prediction")

    st.write(f"Expected Expense Next Month: ₹{int(future_expense)}")
    st.write(f"Expected Savings: ₹{int(future_savings)}")

    if future_savings < 0:
        st.error("🚨 You may go into deficit next month")
    elif future_savings < income * 0.2:
        st.warning("⚠️ Savings may be low")
    else:
        st.success("✅ Financial condition looks stable")

    # -------------------------
    # INSIGHTS
    # -------------------------
    st.subheader("🧠 Insights")

    highest = max(values)
    highest_category = categories[values.index(highest)]

    st.write(f"You spend the most on **{highest_category}**")

    if savings_ratio < 0:
        st.write("👉 Reduce expenses immediately")
    elif savings_ratio < 0.2:
        st.write("👉 Try to save at least 20% of income")
    else:
        st.write("👉 Your financial habits are good")
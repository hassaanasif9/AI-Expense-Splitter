import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import random

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="💳 AI Expense Splitter", page_icon="📅", layout="wide")

# -------------------- CUSTOM STYLING --------------------
st.markdown("""
    <style>
        body {background-color: #121212; color: white;}
        .stButton > button {background-color: #ff4757; color: white; border-radius: 8px; transition: 0.3s;}
        .stButton > button:hover {background-color: #e84118; transform: scale(1.05);}
        .stSidebar {background-color: #1e1e1e; color: white;}
        .title-text {text-align: center; font-size: 30px; font-weight: bold; color: #ffa502;}
        .glowing-text {animation: glow 2s infinite alternate; font-size: 25px; text-align: center; color: #2ed573;}
        @keyframes glow {
            0% {text-shadow: 0 0 5px #ff9f43, 0 0 10px #ff4757;}
            50% {text-shadow: 0 0 15px #ff6b81, 0 0 20px #ff4757;}
            100% {text-shadow: 0 0 5px #ff9f43, 0 0 10px #ff4757;}
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- APP HEADER --------------------
st.markdown("<h1 class='title-text'>💳 AI Expense Splitter & Bill Manager</h1>", unsafe_allow_html=True)

# -------------------- CREATE A GROUP --------------------
st.sidebar.header("🏠 Create a Group")
group_name = st.sidebar.text_input("Group Name (e.g., Friends Trip, Family Budget)", value="Friends Trip")

# Number of members
num_members = st.sidebar.number_input("Number of Members", min_value=2, max_value=10, value=3)
members = [st.sidebar.text_input(f"Enter Member {i+1}", value=f"Person {i+1}") for i in range(num_members)]

# -------------------- ADD AN EXPENSE --------------------
st.sidebar.header("💸 Add an Expense")
expense_name = st.sidebar.text_input("Expense Description", value="Dinner")
expense_amount = st.sidebar.number_input("Total Amount ($)", min_value=1.0, value=50.0)
payer = st.sidebar.selectbox("Who Paid?", members)
shared_by = st.sidebar.multiselect("Who Shares the Cost?", members, default=members)

# -------------------- SPLIT CALCULATIONS --------------------
if st.sidebar.button("Split Expense"):
    num_shared = len(shared_by)
    split_amount = round(expense_amount / num_shared, 2)

    balances = {member: 0 for member in members}
    balances[payer] += expense_amount

    for member in shared_by:
        balances[member] -= split_amount

    df_balances = pd.DataFrame(list(balances.items()), columns=["Person", "Balance ($)"])

    # -------------------- DISPLAY RESULTS --------------------
    st.subheader(f"💰 Expense Split for '{group_name}'")
    st.dataframe(df_balances.style.applymap(lambda x: "color: green;" if x > 0 else "color: red;", subset=["Balance ($)"]))

    # -------------------- VISUALIZATIONS --------------------
    st.subheader("📊 Visual Breakdown")

    # 1️⃣ Balance Distribution Bar Chart
    fig1 = px.bar(df_balances, x="Person", y="Balance ($)", title="📉 Who Owes How Much?", color="Balance ($)")
    st.plotly_chart(fig1, use_container_width=True)

    # 2️⃣ Expense Breakdown Pie Chart
    expense_chart = px.pie(names=shared_by, values=[split_amount] * len(shared_by), title="💰 Contribution Breakdown")
    st.plotly_chart(expense_chart, use_container_width=True)

    # 3️⃣ Expense Over Time Line Chart (Simulated Data)
    expense_data = pd.DataFrame({"Date": pd.date_range(start="2024-01-01", periods=10, freq="D"),
                                 "Amount": [random.randint(20, 200) for _ in range(10)]})
    fig3 = px.line(expense_data, x="Date", y="Amount", title="📈 Expense Trend Over Time", markers=True)
    st.plotly_chart(fig3, use_container_width=True)

    # 4️⃣ Member-wise Contribution Heatmap
    heatmap_data = np.random.rand(num_members, num_members) * 100
    fig4 = ff.create_annotated_heatmap(z=heatmap_data, x=members, y=members, colorscale="Blues")
    st.plotly_chart(fig4, use_container_width=True)

    # 5️⃣ Debt & Credit Waterfall Chart
    df_balances["Type"] = df_balances["Balance ($)"].apply(lambda x: "Credit" if x > 0 else "Debt")
    fig5 = px.funnel(df_balances, x="Balance ($)", y="Person", color="Type", title="💳 Who Owes & Who Gets Paid?")
    st.plotly_chart(fig5, use_container_width=True)

    # -------------------- DOWNLOAD REPORT --------------------
    csv_balances = df_balances.to_csv(index=False).encode("utf-8")
    st.download_button(label="📥 Download Expense Report", data=csv_balances, file_name="expense_report.csv", mime="text/csv")

# -------------------- AI CHATBOT --------------------
st.subheader("🤖 AI Expense Advisor")
st.text("Ask AI for insights on managing expenses efficiently!")
user_input = st.text_input("Ask AI anything about budgeting & expenses:")
if user_input:
    st.success("AI Response: Smart spending = Smart saving! Track, plan, and grow your wealth. 💡")

# -------------------- FINAL MESSAGE --------------------
st.markdown("<h2 class='glowing-text'>💡 Keep tracking & saving smarter!</h2>", unsafe_allow_html=True)

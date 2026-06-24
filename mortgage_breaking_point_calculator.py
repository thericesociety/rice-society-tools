import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Mortgage Breaking Point Calculator",
    page_icon="🍚",
    layout="centered"
)

def monthly_repayment(loan_amount, annual_rate, years):
    monthly_rate = annual_rate / 100 / 12
    months = years * 12

    if monthly_rate == 0:
        return loan_amount / months

    return loan_amount * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)

st.title("🍚 Mortgage Breaking Point Calculator")

st.write(
    "Work out how your monthly repayment may change if interest rates rise."
)

st.caption("Educational tool only. Not financial advice.")

loan_amount = st.number_input(
    "Loan balance",
    min_value=0,
    value=800000,
    step=10000,
    format="%d"
)

remaining_years = st.number_input(
    "Remaining loan term in years",
    min_value=1,
    max_value=40,
    value=25,
    step=1
)

current_rate = st.number_input(
    "Current interest rate (%)",
    min_value=0.0,
    value=6.0,
    step=0.1
)

st.subheader("Repayment scenarios")

rate_scenarios = [
    current_rate,
    current_rate + 0.5,
    current_rate + 1.0,
    current_rate + 1.5,
    current_rate + 2.0,
]

rows = []

current_repayment = monthly_repayment(loan_amount, current_rate, remaining_years)

for rate in rate_scenarios:
    repayment = monthly_repayment(loan_amount, rate, remaining_years)
    rows.append({
        "Interest rate": f"{rate:.2f}%",
        "Monthly repayment": f"${repayment:,.0f}",
        "Increase vs current": f"${repayment - current_repayment:,.0f}"
    })

df = pd.DataFrame(rows)

st.table(df)

st.subheader("Find your breaking point")

comfort_limit = st.number_input(
    "At what monthly repayment would you feel financially uncomfortable?",
    min_value=0,
    value=int(current_repayment + 1000),
    step=100
)

st.write("Your estimated current repayment:")

st.header(f"${current_repayment:,.0f} / month")

if comfort_limit <= current_repayment:
    st.warning("You may already be near or above your comfort limit.")
else:
    st.success(
        f"You have about ${comfort_limit - current_repayment:,.0f} per month before reaching your stated limit."
    )

st.divider()

st.write(
    "The point is not to predict rates perfectly. "
    "The point is to understand what you can comfortably survive if rates move against you."
)

st.caption("The Rice Society 🍚 Make sense of money and the world around us — one grain at a time.")

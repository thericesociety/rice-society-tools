import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Mortgage Breaking Point Calculator",
    page_icon="🍚",
    layout="centered",
)

BRAND_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans:wght@400;500;600;700&display=swap');

.stApp {
    background-color: #FFF6E9;
}

html, body, [class*="css"] {
    font-family: Inter, Noto Sans, Arial, sans-serif;
    color: #111111;
}

.block-container {
    max-width: 720px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.rice-brand-header {
    background-color: #C8102E;
    color: #FFFFFF;
    text-align: center;
    padding: 0.875rem 1.25rem;
    border-radius: 12px;
    margin-bottom: 1.25rem;
    font-weight: 600;
    font-size: 1.125rem;
    letter-spacing: 0.01em;
}

.rice-disclaimer {
    color: #444444;
    font-size: 0.875rem;
    margin: 0.25rem 0 1.25rem 0;
}

.rice-tagline {
    color: #444444;
    font-size: 0.875rem;
    text-align: center;
    margin-top: 1.5rem;
}

h1, h2, h3 {
    color: #C8102E !important;
    font-weight: 700 !important;
}

h1 {
    font-size: 1.75rem !important;
    margin-bottom: 0.5rem !important;
}

h2 {
    font-size: 1.25rem !important;
}

h3 {
    font-size: 1.1rem !important;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF;
    border-radius: 16px !important;
    border: 1px solid rgba(200, 16, 46, 0.12) !important;
    padding: 0.75rem 1rem 1rem 1rem;
    box-shadow: 0 2px 10px rgba(17, 17, 17, 0.06);
    margin-bottom: 0.75rem;
}

[data-testid="stNumberInput"] {
    color-scheme: light;
}

[data-testid="stNumberInput"] label,
[data-testid="stMarkdownContainer"] p {
    color: #111111;
}

[data-testid="stNumberInput"] [data-baseweb="input"],
[data-testid="stNumberInput"] [data-baseweb="input"] > div,
[data-testid="stNumberInputField"],
[data-testid="stNumberInput"] input {
    background-color: #FFFFFF !important;
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
    caret-color: #111111 !important;
    border: 1px solid rgba(17, 17, 17, 0.18) !important;
    border-radius: 8px !important;
    box-shadow: none !important;
}

[data-testid="stNumberInput"] [data-baseweb="input"]:focus-within,
[data-testid="stNumberInput"] input:focus {
    border-color: rgba(200, 16, 46, 0.45) !important;
    box-shadow: 0 0 0 1px rgba(200, 16, 46, 0.2) !important;
    outline: none !important;
}

[data-testid="stNumberInput"] button {
    background-color: #FFFFFF !important;
    color: #111111 !important;
    border: 1px solid rgba(17, 17, 17, 0.18) !important;
    box-shadow: none !important;
}

[data-testid="stNumberInput"] button:hover,
[data-testid="stNumberInput"] button:focus {
    background-color: #F7F7F7 !important;
    color: #111111 !important;
    border-color: rgba(17, 17, 17, 0.25) !important;
}

[data-testid="stNumberInput"] button svg,
[data-testid="stNumberInput"] button path {
    fill: #111111 !important;
    stroke: #111111 !important;
}

[data-testid="stTable"] {
    overflow-x: auto;
}

[data-testid="stTable"] table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.95rem;
}

[data-testid="stTable"] th {
    background-color: rgba(200, 16, 46, 0.08);
    color: #C8102E;
    font-weight: 600;
}

[data-testid="stTable"] th,
[data-testid="stTable"] td {
    padding: 0.625rem 0.75rem;
    border-bottom: 1px solid rgba(17, 17, 17, 0.08);
}

.rice-highlight {
    background-color: #FFFFFF;
    border-radius: 16px;
    border: 1px solid rgba(200, 16, 46, 0.12);
    box-shadow: 0 2px 10px rgba(17, 17, 17, 0.06);
    padding: 1rem 1.25rem;
    margin: 0.75rem 0 1rem 0;
    text-align: center;
}

.rice-highlight h1 {
    margin: 0 !important;
    font-size: 2rem !important;
}

@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 1rem !important;
    }

    .rice-brand-header {
        font-size: 1rem;
        padding: 0.75rem 1rem;
        border-radius: 10px;
    }

    h1 {
        font-size: 1.5rem !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 12px !important;
        padding: 0.625rem 0.75rem 0.875rem 0.75rem;
    }

    .rice-highlight h1 {
        font-size: 1.625rem !important;
    }

    [data-testid="stTable"] table {
        font-size: 0.875rem;
    }
}
</style>
"""

st.markdown(BRAND_CSS, unsafe_allow_html=True)
st.markdown('<div class="rice-brand-header">🍚 The Rice Society</div>', unsafe_allow_html=True)


def monthly_repayment(loan_amount, annual_rate, years):
    monthly_rate = annual_rate / 100 / 12
    months = years * 12

    if monthly_rate == 0:
        return loan_amount / months

    return loan_amount * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)


st.title("Mortgage Breaking Point Calculator")

st.write(
    "Work out how your monthly repayment may change if interest rates rise."
)

st.markdown(
    '<p class="rice-disclaimer">Educational only. Not financial advice.</p>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    loan_amount = st.number_input(
        "Loan balance",
        min_value=0,
        value=800000,
        step=10000,
        format="%d",
    )

    remaining_years = st.number_input(
        "Remaining loan term in years",
        min_value=1,
        max_value=40,
        value=25,
        step=1,
    )

    current_rate = st.number_input(
        "Current interest rate (%)",
        min_value=0.0,
        value=6.0,
        step=0.1,
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
        "Increase vs current": f"${repayment - current_repayment:,.0f}",
    })

df = pd.DataFrame(rows)

with st.container(border=True):
    st.table(df)

st.subheader("Find your breaking point")

with st.container(border=True):
    comfort_limit = st.number_input(
        "At what monthly repayment would you feel financially uncomfortable?",
        min_value=0,
        value=int(current_repayment + 1000),
        step=100,
    )

    st.write("Your estimated current repayment:")

    st.markdown(
        f'<div class="rice-highlight"><h1>${current_repayment:,.0f} / month</h1></div>',
        unsafe_allow_html=True,
    )

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

st.markdown(
    '<p class="rice-tagline">The Rice Society 🍚 Make sense of money and the world around us — one grain at a time.</p>',
    unsafe_allow_html=True,
)

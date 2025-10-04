import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Mortgage Repayment Calculator")

st.write("## Input your mortgage details below:")
# Input fields
col1, col2 = st.columns(2)
home_value = col1.number_input("Home Value ($)", min_value=0.0, value=300000.0)
deposit = col1.number_input("Deposit ($)", min_value=0.0, value=100000.0)
interest_rate = col2.number_input("Interest Rate (%)", min_value=0.0, value=5.5)
loan_term = col2.number_input("Loan Term (years)", min_value=1, value=30)

# Calculate loan amount
loan_amount = home_value - deposit
monthly_interest_rate = (interest_rate / 100) / 12
number_of_payments = loan_term * 12
monthly_payment = (
    loan_amount
    * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
    / ((1 + monthly_interest_rate) ** number_of_payments - 1)
)

# Display for repayment details
total_payment = monthly_payment * number_of_payments
total_interest = total_payment - loan_amount

st.write("## Repayment Details:")
col1, col2, col3 = st.columns(3)
col1.metric("Monthly Payment ($)", f"${monthly_payment:,.2f}")
col2.metric("Total Payment ($)", f"${total_payment:,.2f}")
col3.metric("Total Interest ($)", f"${total_interest:,.2f}")

# Amortization schedule
schedule = []
remaining_balance = loan_amount

for i in range(1, number_of_payments + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i / 12)
    schedule.append(
        [
            i,
            monthly_payment,
            principal_payment,
            interest_payment,
            remaining_balance,
            year,
        ]
    )

df = pd.DataFrame(
    schedule,
    columns=[
        "Month",
        "Payment",
        "Principal Payment",
        "Interest Payment",
        "Remaining Balance",
        "Year",
    ],
)

st.write("## Payment Schedule")
payments_df = df[["Year", "Remaining Balance"]].groupby("Year").mean().min()
st.line_chart(payments_df)

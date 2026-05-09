# Expense-Calc
import streamlit as st
from streamlit_gsheets import GSheetsConnection
st.title("Family Expense Tracker")
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()
with st.form("expense_form"):
    category = st.selectbox("Category", ["Food", "Utilities", "Entertainment"])
    amount = st.number_input("Amount", min_value=0.0)
    submit = st.form_submit_button("Add Expense") 
                   if submit:
          new_data = {"Category": category, "Amount": amount}
          st.success("Expense added!")

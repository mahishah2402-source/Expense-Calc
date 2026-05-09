import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Set up the page title and icon
st.set_page_config(page_title="Joint Expense Tracker", page_icon="💰")

st.title("💰 Our Joint Expense Tracker")
st.write("Enter your expenses below to sync with the group.")

# 1. Establish Connection
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Read Existing Data
df = conn.read(ttl="0s") # ttl="0s" ensures it fetches fresh data every time

# 3. Create the Input Form
with st.form(key="expense_form"):
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Food", "Utilities", "Entertainment", "Other"])
    amount = st.number_input("Amount", min_value=0, step=0.01)
    note = st.text_input("Note (Optional)")
    
    submit_button = st.form_submit_button(label="Add Expense")

# 4. Logic to Update Google Sheets
if submit_button:
    if amount > 0:
        # Create a new row of data
        new_row = pd.DataFrame([{
            "Date": date.strftime("%Y-%m-%d"),
            "Category": category,
            "Amount": amount,
            "Note": note
        }])
        
        # Add new row to existing data
        updated_df = pd.concat([df, new_row], ignore_index=True)
        
        # Update the Google Sheet
        conn.update(data=updated_df)
        st.success("✅ Expense added and synced!")
        st.rerun() # Refresh to show new data
    else:
        st.warning("Please enter an amount greater than 0.")

# 5. Display Summary
st.divider()
st.subheader("Monthly Summary")
total_spent = df["Amount"].sum()
st.metric("Total Spent", f"${total_spent:.2f}")

st.dataframe(df.sort_index(ascending=False), use_container_width=True)

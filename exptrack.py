import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Page Setup
st.set_page_config(page_title="Joint Expense Tracker", page_icon="💰")

st.title("💰 Shared Expense Tracker")

# --- INPUT SECTION ---
# REPLACE THIS URL with your actual Google Form link
form_url = "https://docs.google.com/spreadsheets/d/188fODm9smP-Cxxp8t7FRyibkPSNMIEiKpP17pff0KmE/edit?usp=sharing"

st.link_button("➕ Add New Expense", form_url, type="primary", use_container_width=True)

st.divider()

# --- DATA SECTION ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(ttl=0)

    if not df.empty:
        # Calculate overall total
        total = df["Amount"].sum()
        st.metric("Total Monthly Spend", f"${total:,.2f}")

        # --- NEW: CATEGORY-WISE SUMMATION ---
        st.subheader("📊 Spending by Category")
        
        # Group by 'Category' and sum the 'Amount'
        # Note: Ensure the column names 'Category' and 'Amount' match your Sheet exactly!
        category_df = df.groupby("Category")["Amount"].sum().reset_index()
        category_df = category_df.sort_values(by="Amount", ascending=False)

        # Create two columns: one for a chart, one for the table
        col1, col2 = st.columns([2, 1])

        with col1:
            # Displays a simple horizontal bar chart
            st.bar_chart(data=category_df, x="Category", y="Amount", color="#ff4b4b")

        with col2:
            # Displays the text-based breakdown
            for index, row in category_df.iterrows():
                st.write(f"**{row['Category']}:** ${row['Amount']:,.2f}")

        st.divider()
        st.subheader("Recent History")
        st.dataframe(df.sort_index(ascending=False), use_container_width=True)
        
    else:
        st.info("No data found. Tap the button above to add your first expense!")
except Exception as e:
    st.error(f"Error: {e}")
    st.info("Double-check that your Google Sheet column headers are exactly 'Category' and 'Amount'.")

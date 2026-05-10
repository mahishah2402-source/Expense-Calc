import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

# 1. Page Setup
st.set_page_config(page_title="Family Expense Tracker", page_icon="₹")

st.title("₹ Shared Expense Tracker")

# --- 2. INPUT BUTTON ---
form_url =  "https://docs.google.com/spreadsheets/d/188fODm9smP-Cxxp8t7FRyibkPSNMIEiKpP17pff0KmE/edit?usp=sharing"
st.link_button("➕ Log New Expense", form_url, type="primary", use_container_width=True)

st.divider()

# --- 3. DATA LOADING ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(ttl=0)

    if not df.empty:
        # Convert Timestamp to datetime objects
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], dayfirst=True)
        
        # Create a formatted date string for display (DD-MM-YYYY)
        df['Date'] = df['Timestamp'].dt.strftime('%d-%m-%Y')
        
        # Create Month for the sidebar filter
        df['Month_Filter'] = df['Timestamp'].dt.strftime('%B %Y')

        # --- 4. SIDEBAR FILTER ---
        st.sidebar.header("📅 Filter Records")
        available_months = df['Month_Filter'].unique()
        selected_month = st.sidebar.selectbox("Select Month", available_months)

        filtered_df = df[df['Month_Filter'] == selected_month]

        # --- 5. RUPEE SUMMARY METRIC ---
        total = filtered_df["Amount"].sum()
        st.metric(f"Total Spent in {selected_month}", f"₹{total:,.2f}")

        # --- 6. CATEGORY PIE CHART ---
        st.subheader(f"📊 {selected_month} Breakdown")
        cat_sum = filtered_df.groupby("Category")["Amount"].sum().reset_index()
        
        fig = px.pie(
            cat_sum, 
            values='Amount', 
            names='Category', 
            color_discrete_sequence=px.colors.sequential.Blues_r,
            hole=0.4
        )
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

        st.divider()
        st.subheader("Transaction History")
        
        # Only show the columns we want in the table, in the order we want
        # We use the new 'Date' column instead of the raw 'Timestamp'
        display_df = filtered_df[['Date', 'Category', 'Amount']]
        if 'Note' in filtered_df.columns: # Add Note if it exists in your form
            display_df = filtered_df[['Date', 'Category', 'Amount', 'Note']]
            
        st.dataframe(display_df.sort_index(ascending=False), use_container_width=True)
    
    else:
        st.info("No records found. Use the button above to log your first expense!")

except Exception as e:
    st.error(f"Error: {e}")

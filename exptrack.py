import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Family Expense Tracker", page_icon="📅")

st.title("📅 Family Expense Dashboard")

# --- 1. INPUT BUTTON ---
form_url = "https://docs.google.com/forms/d/e/YOUR_FORM_ID/viewform"
st.link_button("➕ Log New Expense", form_url, type="primary", use_container_width=True)

# --- 2. DATA LOADING ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(ttl=0)

    if not df.empty:
        # Convert Timestamp to actual Python datetime objects
        # Google Forms usually calls this 'Timestamp'
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df['Month'] = df['Timestamp'].dt.strftime('%B %Y')

        # --- 3. CALENDAR / MONTH FILTER ---
        st.sidebar.header("Filter by Date")
        available_months = df['Month'].unique()
        selected_month = st.sidebar.selectbox("Select Month", available_months)

        # Filter the data based on selection
        filtered_df = df[df['Month'] == selected_month]

        # --- 4. DISPLAY SUMMARY ---
        total = filtered_df["Amount"].sum()
        st.metric(f"Total for {selected_month}", f"${total:,.2f}")

        # Category Breakdown
        st.subheader(f"📊 {selected_month} Breakdown")
        cat_sum = filtered_df.groupby("Category")["Amount"].sum().reset_index()
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.bar_chart(data=cat_sum, x="Category", y="Amount", color="#29b5e8")
        with col2:
            for _, row in cat_sum.iterrows():
                st.write(f"**{row['Category']}:** ${row['Amount']:,.2f}")

        st.divider()
        st.subheader("Full History")
        st.dataframe(filtered_df.sort_values("Timestamp", ascending=False), use_container_width=True)
    
    else:
        st.info("No data yet! Use the button above to log your first expense.")

except Exception as e:
    st.error(f"Waiting for data... Ensure your Sheet has 'Timestamp', 'Category', and 'Amount' columns.")

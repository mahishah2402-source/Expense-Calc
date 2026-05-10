import streamlit as st from streamlit_gsheets 
import GSheetsConnection
import pandas as pd
import plotly.express as px

# 1. Page Setup
st.set_page_config(page_title="Family Expense Tracker", page_icon="₹")

st.title("₹ Shared Expense Tracker")

# --- 2. INPUT BUTTON ---
# REPLACE THIS URL with your actual Google Form link
form_url = "https://docs.google.com/spreadsheets/d/188fODm9smP-Cxxp8t7FRyibkPSNMIEiKpP17pff0KmE/edit?usp=sharing"
st.link_button("➕ Log New Expense", form_url, type="primary", use_container_width=True)

st.divider()

# --- 3. DATA LOADING ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(ttl=0)

    if not df.empty:
        # Convert Google's 'Timestamp' to a Date format automatically
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df['Month'] = df['Timestamp'].dt.strftime('%B %Y')

        # --- 4. SIDEBAR FILTER ---
        st.sidebar.header("📅 Filter Records")
        available_months = df['Month'].unique()
        selected_month = st.sidebar.selectbox("Select Month", available_months)

        filtered_df = df[df['Month'] == selected_month]

        # --- 5. RUPEE SUMMARY METRIC ---
        total = filtered_df["Amount"].sum()
        st.metric(f"Total Spent in {selected_month}", f"₹{total:,.2f}")

        # --- 6. CATEGORY PIE CHART (Shades of Blue) ---
        st.subheader(f"📊 {selected_month} Category Breakdown")
        cat_sum = filtered_df.groupby("Category")["Amount"].sum().reset_index()
        
        # Create the Pie Chart using Plotly
        fig = px.pie(
            cat_sum, 
            values='Amount', 
            names='Category', 
            color_discrete_sequence=px.colors.sequential.Blues_r, # Shades of blue
            hole=0.4 # This makes it a donut chart, remove for full pie
        )
        
        # Update chart layout for better mobile viewing
        fig.update_layout(showlegend=True, margin=dict(t=0, b=0, l=0, r=0))
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)

        st.divider()
        st.subheader("Transaction History")
        st.dataframe(filtered_df.sort_values("Timestamp", ascending=False), use_container_width=True)
    
    else:
        st.info("No records found. Use the button above to log your first expense!")

except Exception as e:
    st.error(f"Error loading data: {e}")

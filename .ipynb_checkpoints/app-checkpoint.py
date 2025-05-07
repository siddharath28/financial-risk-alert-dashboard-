import streamlit as st
import pandas as pd

# Load your data
df = pd.read_csv('data/all_financial_news.csv')

# Get latest date
latest_date = df['date'].max()
latest_data = df[df['date'] == latest_date]

# Check for risk alert
if latest_data['risk_alert'].any():
    st.error("🚨 Risk Alert Triggered!")
    st.write(latest_data[latest_data['risk_alert'] == 1])
else:
    st.success("✅ No Risk Alert Today.")

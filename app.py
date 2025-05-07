import streamlit as st
import pandas as pd
import plotly.express as px

# ✅ Set page config first
st.set_page_config(page_title="Financial Risk Alert Dashboard", layout="wide")

# --- Load Data ---
df = pd.read_csv("data/all_financial_news.csv")
df['date'] = pd.to_datetime(df['date'])

# --- Sidebar ---
st.sidebar.title("📊 Filters")

# Dropdown for company/source
company_list = sorted(df['source'].dropna().unique())
selected_company = st.sidebar.selectbox("Select News Source", ["All"] + company_list)

# Toggle for historical view
show_history = st.sidebar.checkbox("📈 Show Historical Sentiment Trend", value=True)

# --- Filter based on selection ---
if selected_company != "All":
    df = df[df['source'] == selected_company]

# --- Latest Risk Alert ---
st.title("🚨 Financial Risk Alert System")

latest_date = df['date'].max()
latest_data = df[df['date'] == latest_date]

st.markdown(f"### 🗓️ Latest News Date: `{latest_date.date()}`")

# Alert Section
if latest_data['risk_alert'].any():
    st.error("🚨 Risk Alert Triggered!")
    st.dataframe(latest_data[latest_data['risk_alert'] == 1][['title', 'source', 'sentiment_score', 'date']])
else:
    st.success("✅ No Risk Alert Detected.")

# --- KPI Cards ---
col1, col2, col3 = st.columns(3)
col1.metric("📰 Total Articles", len(df))
col2.metric("⚠️ Total Risk Alerts", int(df['risk_alert'].sum()))
col3.metric("🧠 Avg Sentiment", f"{df['sentiment_score'].mean():.2f}")

# --- Historical View Section ---
if show_history:
    st.markdown("## 📉 Sentiment Over Time")
    sentiment_trend = df.groupby('date')['sentiment_score'].mean().reset_index()
    fig = px.line(sentiment_trend, x='date', y='sentiment_score', title="Average Sentiment Trend")
    st.plotly_chart(fig, use_container_width=True)

# --- Raw Table ---
st.markdown("## 📃 All News Records")
st.dataframe(df[['title', 'source', 'sentiment_score', 'risk_alert', 'date']].sort_values(by='date', ascending=False))

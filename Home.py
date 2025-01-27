import streamlit as st
from datetime import datetime
import pandas as pd
from utils.db_pool import DatabasePool
from utils.models import MigratedCoin, Tweet
from utils.scheduler import TaskScheduler
from utils.data_fetcher import fetch_migrated_coins, update_market_data
from utils.sentiment_analyzer import analyze_sentiment
from utils.log_util import setup_logging
import plotly.express as px

# Initialize database and logger
db_pool = DatabasePool()
logger = setup_logging(__name__, db_session_maker=db_pool.SessionLocal)

# Initialize scheduler
scheduler = TaskScheduler()
scheduler.start()
logger.info("Scheduler started")

# Streamlit UI
st.title("Crypto Migration Monitor")

# Sidebar
st.sidebar.header("Dashboard Controls")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    ["Last 24 Hours", "Last Week", "Last Month", "All Time"]
)

# Task Control Section in Sidebar
st.sidebar.header("Task Controls")

# Individual Task Buttons
st.sidebar.subheader("Run Individual Tasks")
if st.sidebar.button("Fetch Migrated Coins"):
    with st.spinner("Fetching migrated coins..."):
        try:
            fetch_migrated_coins()
            st.success("Fetch completed!")
            logger.info("Manual fetch_migrated_coins completed successfully")
        except Exception as e:
            st.error("Fetch failed!")
            logger.error(f"Manual fetch_migrated_coins failed: {str(e)}", exc_info=True)

if st.sidebar.button("Update Market Data"):
    with st.spinner("Updating market data..."):
        try:
            update_market_data()
            st.success("Market data updated!")
            logger.info("Manual update_market_data completed successfully")
        except Exception as e:
            st.error("Update failed!")
            logger.error(f"Manual update_market_data failed: {str(e)}", exc_info=True)

if st.sidebar.button("Analyze Sentiment"):
    with st.spinner("Analyzing sentiment..."):
        try:
            analyze_sentiment()
            st.success("Sentiment analysis completed!")
            logger.info("Manual sentiment analysis completed successfully")
        except Exception as e:
            st.error("Analysis failed!")
            logger.error(f"Manual sentiment analysis failed: {str(e)}", exc_info=True)

# Scheduler Control
st.sidebar.subheader("Scheduler Control")
scheduler_status = st.sidebar.empty()
if scheduler.is_running():
    if st.sidebar.button("Stop Scheduler"):
        scheduler.stop()
        scheduler_status.info("Scheduler stopped")
        logger.info("Scheduler stopped manually")
else:
    if st.sidebar.button("Start Scheduler"):
        scheduler.start()
        scheduler_status.info("Scheduler running")
        logger.info("Scheduler started manually")

# Main dashboard
col1, col2 = st.columns(2)

with col1:
    st.subheader("Active Tasks")
    task_status = scheduler.get_task_status()
    tasks_df = pd.DataFrame([
        {
            'Task': task,
            'Schedule': info['schedule'],
            'Last Run': info['last_run'].strftime("%H:%M:%S") if info['last_run'] else "Never",
            'Status': info['status']
        }
        for task, info in task_status.items()
    ])
    st.dataframe(tasks_df)

with col2:
    st.subheader("System Status")
    st.metric("Database Connections", "5/10")
    st.metric("API Rate Limit", "95%")

# Data Overview
st.header("Data Overview")

# Use database session to fetch data
try:
    with db_pool.get_session() as session:
        # Recent migrations
        migrations = session.query(MigratedCoin).order_by(
            MigratedCoin.migration_date.desc()
        ).limit(5).all()
        
        if migrations:
            migrations_df = pd.DataFrame([{
                'Coin': m.coin_symbol,
                'Market Cap': f"${m.market_cap:,.2f}",
                'Volume': f"${m.volume:,.2f}",
                'Migration Date': m.migration_date.strftime("%Y-%m-%d %H:%M")
            } for m in migrations])
            
            st.subheader("Recent Migrations")
            st.dataframe(migrations_df)
        
        # Sentiment Analysis
        sentiment_data = session.query(
            Tweet.coin_id,
            MigratedCoin.coin_symbol,
            Tweet.sentiment
        ).join(MigratedCoin).all()
        
        if sentiment_data:
            sentiment_df = pd.DataFrame(sentiment_data)
            avg_sentiment = sentiment_df.groupby('coin_symbol')['sentiment'].mean().reset_index()
            
            st.subheader("Sentiment Analysis")
            fig = px.bar(avg_sentiment, x='coin_symbol', y='sentiment',
                        title='Average Sentiment by Coin')
            st.plotly_chart(fig)
except Exception as e:
    logger.error("Failed to fetch dashboard data", exc_info=True)
    st.error("Failed to load dashboard data. Please check the logs.")

# Market Overview
st.header("Market Overview")
col3, col4 = st.columns(2)

with col3:
    st.subheader("Top Performers")
    # Add performance metrics visualization

with col4:
    st.subheader("Volume Distribution")
    # Add volume distribution chart

# Alerts and Notifications
st.header("Alerts")
alerts = [
    "High sentiment spike detected for COIN1",
    "New migration detected: COIN2",
    "Unusual volume increase: COIN3"
]
for alert in alerts:
    st.warning(alert)

# Footer
st.markdown("---")
st.markdown("Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Add refresh button
if st.button("Refresh Data"):
    logger.info("Manual dashboard refresh triggered")
    st.experimental_rerun()

"""Visualisation helper functions for news article analytics using Streamlit."""
import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime


def plot_all_categories_trend(weekly_stats, begin_date=None, end_date=None):
    """
    Display line chart comparing all categories over the specified date range using Streamlit.
    
    Args:
        weekly_stats (dict): Output from get_weekly_category_stats()
        begin_date (date): Start date for filtering (optional)
        end_date (date): End date for filtering (optional)
    """
    # Prepare data for multi-line chart
    data = []
    for category, stats in weekly_stats.items():
        daily_data = stats['daily_breakdown']
        for date_str, count in sorted(daily_data.items()):
            # Parse date and filter if bounds provided
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            if begin_date and date_obj < begin_date:
                continue
            if end_date and date_obj > end_date:
                continue
            
            data.append({
                'Date': date_str,
                'Articles': count,
                'Category': category
            })
    
    if not data:
        st.warning("No data available for the specified date range.")
        return
    
    df = pd.DataFrame(data)
    
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('Date:T', title='Date'),
        y=alt.Y('Articles:Q', title='Number of Articles'),
        color=alt.Color('Category:N', title='Category'),
        tooltip=['Date:T', 'Articles:Q', 'Category:N']
    ).properties(
        width=900,
        height=500,
        title='Article Trends by Category (Past 3 Weeks)'
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)

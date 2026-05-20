"""
Example usage: Using the updated API module with visualization.

This shows how to fetch articles and visualize them by category for the week.
"""

from src.api import NewsScraper
from src.components import (
    plot_all_categories_trend
)

# Example implementation for Streamlit app
def display_weekly_analytics(scraper, category):
    """
    Fetch articles and display weekly analytics.
    
    Args:
        scraper (NewsScraper): Initialized scraper instance
        category (str): Category to fetch articles for
    """
    import streamlit as st
    
    # Fetch articles
    articles = scraper.fetch_all_news(category)
    
    if not articles:
        st.warning("No articles found for this category.")
        return
    
    # Get statistics
    weekly_stats = scraper.get_weekly_category_stats(articles)
    
    # Display stats table
    st.subheader("📊 Weekly Statistics")
    df = export_stats_to_dataframe(weekly_stats)
    st.dataframe(df, use_container_width=True)
    
    # Display visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Articles by Category")
        fig1 = plot_articles_by_category(weekly_stats)
        st.pyplot(fig1)
    
    with col2:
        st.subheader("📊 Average per Day")
        fig2 = plot_category_comparison(weekly_stats)
        st.pyplot(fig2)
    
    # Display daily trends for each category
    st.subheader("📅 Daily Trends by Category")
    selected_category = st.selectbox("Select category to view daily trend:", list(weekly_stats.keys()))
    
    if selected_category:
        fig3 = plot_category_daily_trend(weekly_stats, selected_category)
        st.pyplot(fig3)
        
        # Show detailed breakdown
        with st.expander(f"📋 Details for {selected_category}"):
            details = weekly_stats[selected_category]
            st.write(f"**Total Articles:** {details['total']}")
            st.write(f"**Average per Day:** {details['avg_per_day']}")
            st.write("**Daily Breakdown:**")
            for date, count in sorted(details['daily_breakdown'].items()):
                st.write(f"  - {date}: {count} articles")

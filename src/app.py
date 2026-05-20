"""Main application orchestrator for the News Aggregator using Streamlit."""
import streamlit as st
from .components.search_controls import render_search_controls
from .components.article_display import render_articles
from .components.analytics_panel import render_analytics_panel


def run_app(news_engine):
    """
    Run the News Aggregator Streamlit application.
    
    Args:
        news_engine (NewsScraper): News scraper instance
    """
    # Page configuration
    st.set_page_config(
        page_title="News Aggregator",
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Title
    st.markdown("# 📰 News Aggregator")
    st.markdown("Search and explore news articles by category")
    
    # Initialize session state
    if "current_articles" not in st.session_state:
        st.session_state.current_articles = []
    if "selected_article" not in st.session_state:
        st.session_state.selected_article = None
    if "show_viz" not in st.session_state:
        st.session_state.show_viz = False
    
    # Render search controls
    selected_category, search_clicked = render_search_controls(news_engine)
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display articles
        render_articles(st.session_state.current_articles)
    
    # Sidebar visualisation
    with col2:
        # Display analytics panel
        render_analytics_panel(st.session_state.current_articles)

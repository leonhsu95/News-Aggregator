"""Search controls component for news category selection and filtering."""
import streamlit as st
from ..config import ALL_CATEGORIES


def render_search_controls(news_engine):
    """
    Render the sidebar search controls for the News Aggregator.
    
    Args:
        news_engine (NewsScraper): News scraper instance
        
    Returns:
        tuple: (selected_category, search_clicked)
    """
    with st.sidebar:
        st.header("Search Controls")
        
        # Category dropdown
        selected_category = st.selectbox(
            "Select news category:",
            ALL_CATEGORIES,
            index=0
        )
        
        # Search button
        search_clicked = st.button("🔍 Search News", use_container_width=True)
        if search_clicked:
            with st.spinner("Loading articles..."):
                results = news_engine.fetch_all_news(selected_category)
                st.session_state.current_articles = results
        
        # Visualization button
        show_viz = st.button("📊 Show Visualization", use_container_width=True)
        if show_viz:
            st.session_state.show_viz = True
        else:
            st.session_state.show_viz = False
    
    return selected_category, search_clicked

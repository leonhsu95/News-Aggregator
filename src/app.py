"""Main application orchestrator for the News Aggregator using Streamlit."""
import os
import streamlit as st
from .components.search_controls import render_search_controls
from .components.article_display import render_articles
from .components.analytics_panel import render_analytics_panel
from .styles_loader import load_all_styles


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
        layout="centered",
        initial_sidebar_state="expanded"
    )

    # Load stylesheets (use compiled CSS if available, otherwise load dynamically)
    css_files = [
        "styles/styles.css",
        "styles/article-display.css",
        "styles/analytics-panel.css"
    ]
    
    compiled_css_path = "styles/compiled.css"
    if os.path.exists(compiled_css_path):
        # Use pre-compiled CSS for better performance
        with open(compiled_css_path) as f:
            combined_css = f.read()
    else:
        # Fallback to dynamic loading
        combined_css = load_all_styles(css_files)
    
    st.markdown(f"<style>{combined_css}</style>", unsafe_allow_html=True)

    st.markdown("""
        <div class="header-container">
            <h1 class="header-title">📰 News Aggregator</h1>
            <p class="header-subtitle">Search and explore news articles by category</p>
        </div>
    """, unsafe_allow_html=True)
    
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

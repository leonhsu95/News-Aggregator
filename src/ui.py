"""GUI module for the News Aggregator application using Streamlit."""
import streamlit as st
import webbrowser
from .config import ALL_CATEGORIES
from .visualizer import NewsVisualizer


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
    
    # Sidebar for controls
    with st.sidebar:
        st.header("Search Controls")
        
        # Category dropdown
        selected_category = st.selectbox(
            "Select news category:",
            ALL_CATEGORIES,
            index=0
        )
        
        # Search button
        if st.button("🔍 Search News", use_container_width=True):
            with st.spinner("Loading articles..."):
                results = news_engine.fetch_all_news(selected_category)
                st.session_state.current_articles = results
        
        # Visualization button
        if st.button("📊 Show Visualization", use_container_width=True):
            st.session_state.show_viz = True
        else:
            st.session_state.show_viz = False
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display articles
        if isinstance(st.session_state.current_articles, str):
            st.error(st.session_state.current_articles)
        elif not st.session_state.current_articles:
            st.info("👈 Select a category and click 'Search News' to get started!")
        else:
            st.markdown(f"### Found {len(st.session_state.current_articles)} articles")
            
            # Display articles as expandable sections
            for i, article in enumerate(st.session_state.current_articles):
                with st.expander(f"📌 {article['title']}", expanded=(i == 0)):
                    st.markdown(f"**Source:** `{article['source'].upper()}`")
                    
                    raw_summary = article.get('summary', 'No summary available!')
                    preview_para = str(raw_summary).split('\n\n')[0]
                    st.markdown(f"**Overview:** {preview_para}")
                    
                    # Display full summary if available
                    if raw_summary and str(raw_summary).strip().lower() not in ["none", "", "No summary available!"]:
                        st.markdown("**Full Summary:**")
                        st.write(raw_summary)
                    else:
                        st.warning("Notice: Full content extraction restricted.")
                    
                    # Article metadata
                    col_url, col_open = st.columns(2)
                    with col_url:
                        st.markdown(f"**URL:** {article['url']}")
                    with col_open:
                        if st.button("🌐 Open in Browser", key=f"btn_{i}"):
                            webbrowser.open(article['url'])
    
    # Sidebar visualization
    with col2:
        if st.session_state.show_viz and st.session_state.current_articles:
            st.subheader("📊 Analytics")
            
            # Display statistics
            visualizer = NewsVisualizer(st.session_state.current_articles)
            stats = visualizer.get_statistics()
            
            if stats:
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                with col_stat1:
                    st.metric("Total Articles", stats["Total Articles"])
                with col_stat2:
                    st.metric("Unique Sources", stats["Unique Sources"])
                with col_stat3:
                    st.metric("Avg Summary Length", f"{stats['Average Summary Length']} chars")
            
            # Visualization tabs
            tab1, tab2, tab3 = st.tabs(["📈 By Source", "📊 Summary Length", "🔤 Top Words"])
            
            with tab1:
                fig1 = visualizer.plot_articles_by_source()
                if fig1:
                    st.pyplot(fig1)
            
            with tab2:
                fig2 = visualizer.plot_summary_length_by_source()
                if fig2:
                    st.pyplot(fig2)
            
            with tab3:
                fig3 = visualizer.plot_top_words()
                if fig3:
                    st.pyplot(fig3)

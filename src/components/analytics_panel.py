"""Analytics panel component for displaying news statistics and visualizations."""
import streamlit as st
from .visualizer import NewsVisualizer


def render_analytics_panel(articles):
    """
    Render analytics dashboard with statistics and visualizations.
    
    Args:
        articles (list): List of article dictionaries
    """
    if articles and st.session_state.get("show_viz", False):
        st.subheader("📊 Analytics")
        
        # Display statistics
        visualizer = NewsVisualizer(articles)
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

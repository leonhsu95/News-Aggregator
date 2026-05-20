"""Article display component for rendering news articles."""
import streamlit as st
import webbrowser


def render_articles(articles):
    """
    Render articles as expandable cards with metadata and links.
    
    Args:
        articles (list): List of article dictionaries
    """
    if isinstance(articles, str):
        st.error(articles)
    elif not articles:
        st.info("👈 Select a category and click 'Search News' to get started!")
    else:
        st.markdown(f"### Found {len(articles)} articles")
        
        # Display articles as expandable sections
        for i, article in enumerate(articles):
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

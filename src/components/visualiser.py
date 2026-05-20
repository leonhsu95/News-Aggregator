"""Data visualisation module for news articles."""

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from collections import Counter
import re


class NewsVisualiser:
    """Creates visualisations for aggregated news articles."""

    def __init__(self, articles):
        """
        Initialise the visualiser with article data.

        Args:
            articles (list): List of article dictionaries.
        """
        self.df = pd.DataFrame(articles)
        # Set a clean matplotlib style
        plt.style.use('seaborn-v0_8-darkgrid')

    def plot_articles_by_source(self):
        """Plot the number of articles from each source."""
        if self.df.empty or "source" not in self.df.columns:
            st.warning("No source data available for visualisation.")
            return None

        source_counts = self.df["source"].value_counts()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        source_counts.plot(kind="bar", ax=ax, color="steelblue")
        ax.set_title("Number of Articles by Source", fontsize=14, fontweight="bold")
        ax.set_xlabel("News Source")
        ax.set_ylabel("Number of Articles")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        
        return fig

    def plot_summary_length_by_source(self):
        """Plot the average summary length for each source."""
        if self.df.empty or "summary" not in self.df.columns or "source" not in self.df.columns:
            st.warning("No summary/source data available for visualisation.")
            return None

        self.df["summary_length"] = self.df["summary"].astype(str).apply(len)
        avg_lengths = self.df.groupby("source")["summary_length"].mean()

        fig, ax = plt.subplots(figsize=(10, 6))
        avg_lengths.plot(kind="bar", ax=ax, color="coral")
        ax.set_title("Average Summary Length by Source", fontsize=14, fontweight="bold")
        ax.set_xlabel("News Source")
        ax.set_ylabel("Average Summary Length (characters)")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        
        return fig

    def plot_top_words(self, num_words=15):
        """Plot the most frequent words in article summaries."""
        if self.df.empty or "summary" not in self.df.columns:
            st.warning("No summary data available.")
            return None

        words = []

        # Common stopwords to ignore
        stopwords = {
            "the", "and", "that", "with", "from", "this",
            "have", "were", "their", "about", "would",
            "there", "which", "when", "what", "your",
            "said", "into", "than", "them", "they",
            "been", "also", "after", "before", "over",
            "more", "news", "article",

            # less meaningful words
            "could", "would", "should", "might", "will",
            "days", "week", "month", "year", "years",
            "time", "times", "people", "officials",
            "according", "reported", "report", "reports",
            "new", "latest", "first", "last", "many",
            "some", "such", "other", "most", "only",
            "just", "like", "make", "made", "using",
            "available", "summary", "extraction", "failed"
        }

        # Extract words from summaries
        text_data = (
            self.df["title"].astype(str) + " " +
            self.df["summary"].astype(str)
        )

        for text in text_data:
            clean_words = re.findall(
                r'\b[a-zA-Z]{4,}\b',
                str(text).lower()
            )

            filtered_words = [
                word for word in clean_words
                if word not in stopwords
            ]

            words.extend(filtered_words)

        # Count frequency
        common_words = Counter(words).most_common(num_words)

        if not common_words:
            st.warning("No valid words found.")
            return None

        labels = [word for word, count in common_words]
        counts = [count for word, count in common_words]

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(labels, counts, color="mediumseagreen")
        ax.set_title(f"Top {num_words} Most Frequent Words", fontsize=14, fontweight="bold")
        ax.set_xlabel("Words")
        ax.set_ylabel("Frequency")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        
        return fig
    
    def plot_articles_per_day(self):
        """Plot the timeline of articles (if date info is available)."""
        if self.df.empty or "date" not in self.df.columns:
            return None
        
        try:
            self.df["date"] = pd.to_datetime(self.df["date"])
            daily_counts = self.df.groupby(self.df["date"].dt.date).size()
            
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(daily_counts.index, daily_counts.values, marker="o", color="royalblue", linewidth=2)
            ax.set_title("Articles Timeline", fontsize=14, fontweight="bold")
            ax.set_xlabel("Date")
            ax.set_ylabel("Number of Articles")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            
            return fig
        except Exception as e:
            st.warning(f"Could not generate timeline visualisation: {e}")
            return None
    
    def get_statistics(self):
        """Get summary statistics about the articles."""
        if self.df.empty:
            return None
        
        stats = {
            "Total Articles": len(self.df),
            "Unique Sources": self.df["source"].nunique() if "source" in self.df.columns else 0,
            "Average Summary Length": int(self.df["summary"].astype(str).apply(len).mean()) if "summary" in self.df.columns else 0,
        }
        
        return stats

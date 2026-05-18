"""Data visualization module for news articles."""

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re


class NewsVisualizer:
    """Creates visualizations for aggregated news articles."""

    def __init__(self, articles):
        """
        Initialise the visualizer with article data.

        Args:
            articles (list): List of article dictionaries.
        """
        self.df = pd.DataFrame(articles)

    def plot_articles_by_source(self):
        """Plot the number of articles from each source."""
        if self.df.empty or "source" not in self.df.columns:
            print("No source data available for visualization.")
            return

        source_counts = self.df["source"].value_counts()

        source_counts.plot(kind="bar")
        plt.title("Number of Articles by Source")
        plt.xlabel("News Source")
        plt.ylabel("Number of Articles")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

    def plot_summary_length_by_source(self):
        """Plot the average summary length for each source."""
        if self.df.empty or "summary" not in self.df.columns or "source" not in self.df.columns:
            print("No summary/source data available for visualization.")
            return

        self.df["summary_length"] = self.df["summary"].astype(str).apply(len)
        avg_lengths = self.df.groupby("source")["summary_length"].mean()

        avg_lengths.plot(kind="bar")
        plt.title("Average Summary Length by Source")
        plt.xlabel("News Source")
        plt.ylabel("Average Summary Length")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

    def plot_top_words(self):
        """Plot the most frequent words in article summaries."""

        if self.df.empty or "summary" not in self.df.columns:
            print("No summary data available.")
            return

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
        common_words = Counter(words).most_common(10)

        if not common_words:
            print("No valid words found.")
            return

        labels = [word for word, count in common_words]
        counts = [count for word, count in common_words]

        plt.figure(figsize=(10, 5))

        plt.bar(labels, counts)

        plt.title("Top 10 Most Frequent Words")
        plt.xlabel("Words")
        plt.ylabel("Frequency")

        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()
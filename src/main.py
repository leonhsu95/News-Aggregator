"""Main entry point for the News Aggregator application."""
import tkinter as tk
from .config import NEWS_API_KEY, NYT_API_KEY, validate_keys
from .api import NewsScraper
from .ui import NewsApp


def main():
    """Launch the News Aggregator application."""
    # Validate API keys before starting
    if not validate_keys():
        print("Error: API keys not configured. Please set NEWS_API_KEY and NYT_API_KEY in .env")
        return

    try:
        # Initialize Tkinter root window
        root = tk.Tk()
        
        # Create news scraper and app
        news_engine = NewsScraper(NEWS_API_KEY, NYT_API_KEY)
        app = NewsApp(root, news_engine)
        
        # Start the GUI event loop
        root.mainloop()

    except Exception as e:
        print(f"App closed. Error: {e}")


if __name__ == "__main__":
    main()

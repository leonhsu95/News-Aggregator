"""GUI module for the News Aggregator application."""
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from .config import ALL_CATEGORIES
from .visualizer import NewsVisualizer

class NewsApp:
    """Tkinter GUI for the News Aggregator."""
    
    def __init__(self, root, news_engine):
        """
        Initialize the GUI.
        
        Args:
            root (tk.Tk): Root window
            news_engine (NewsScraper): News scraper instance
        """
        self.root = root
        self.news_engine = news_engine
        self.current_article = []
        
        self._setup_window()
        self._create_widgets()

    def _setup_window(self):
        """Configure the main window."""
        self.root.title("News Scrapper")
        self.root.geometry("800x600")

    def _create_widgets(self):
        """Create and layout GUI widgets."""
        # Title label
        tk.Label(
            self.root,
            text="Select the news category: ",
            font=("Times New Roman", 14, "bold")
        ).pack(pady=10)

        # Category dropdown
        self.dropdown = ttk.Combobox(
            self.root,
            values=ALL_CATEGORIES,
            state="readonly"
        )
        self.dropdown.set("General")
        self.dropdown.pack()

        # Search button
        tk.Button(
            self.root,
            text="Search News",
            command=self.handle_search,
            bg="blue",
            fg="white",
            font=("Times New Roman", 14, "bold")
        ).pack(pady=10)

        # Display frame with scrollbar
        self.display_frame = tk.Frame(self.root)
        self.display_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.scrollbar = tk.Scrollbar(self.display_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.display = tk.Text(
            self.display_frame,
            wrap=tk.WORD,
            padx=15,
            pady=15,
            font=("Times New Roman", 12),
            yscrollcommand=self.scrollbar.set
        )
        self.display.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.display.yview)
        
        # Configure text tags
        self.display.tag_config("bold_blue", foreground="blue", underline=True, font=("Times New Roman", 12, "bold"))
        self.display.tag_config("source_tag", foreground="green", font=("Times New Roman", 10, "italic"))
        self.display.tag_config("hint", foreground="purple", font=("Times New Roman", 10, "italic"))
        
        self.display.config(state="disabled")

    def handle_search(self):
        """Handle search button click event."""
        selected_category = self.dropdown.get()
        self.display.config(state="normal")
        self.display.delete("1.0", tk.END)
        self.display.insert(tk.END, "Loading...\n")
        self.root.update()
        
        results = self.news_engine.fetch_all_news(selected_category)
        self.current_article = results

        self.display.delete("1.0", tk.END)
        
        if isinstance(results, str):
            messagebox.showerror("Error", results)
        elif not results:
            self.display.insert(tk.END, "No articles found for this category. Try another category!")
        else:
            self._display_articles(results)

        self.display.config(state="disabled")

    def _display_articles(self, articles):
        """
        Display articles in the text widget.
        
        Args:
            articles (list): List of article dictionaries
        """
        for i, news in enumerate(articles):
            tag_name = f"article_{i}"
            self.display.insert(tk.END, f"Title: {news['title']}\n", tag_name)
            self.display.tag_config(tag_name, foreground="blue", underline=True, font=("Times New Roman", 12, "bold"))
            
            self.display.insert(tk.END, f"Source: {news['source'].upper()}\n", "source_tag")

            raw_summary = news.get('summary', 'No summary available!')
            preview_para = str(raw_summary).split('\n\n')[0]
            self.display.insert(tk.END, f"Overview: {preview_para}\n")
            
            self.display.insert(tk.END, "Double-click the title to read more...\n\n", "hint")
            self.display.insert(tk.END, "="*50 + "\n\n")
            
            # Make title clickable
            self.display.tag_bind(tag_name, "<Double-1>", lambda e, idx=i: self.show_full_article(idx))
            self.display.tag_bind(tag_name, "<Enter>", lambda e: self.display.config(cursor="hand2"))
            self.display.tag_bind(tag_name, "<Leave>", lambda e: self.display.config(cursor=""))

    def show_full_article(self, index):
        """
        Display full article in a new window.
        
        Args:
            index (int): Index of article in current_article list
        """
        article = self.current_article[index]
        new_window = tk.Toplevel(self.root)
        new_window.title(article['title'])
        new_window.geometry("800x500")

        # Header with title
        tk.Label(
            new_window,
            text=article['title'],
            font=("Times New Roman", 16, "bold"),
            wraplength=600,
            justify="left",
            fg="#1227AF"
        ).pack(pady=10, padx=20)

        # Open in browser button
        tk.Button(
            new_window,
            text="Open in Browser",
            bg="orange",
            fg="black",
            font=("Times New Roman", 16, "bold"),
            command=lambda: webbrowser.open(article['url'])
        ).pack(pady=5)

        # Scrollable text display
        text = tk.Text(new_window, wrap=tk.WORD, padx=20, pady=25, font=("Times New Roman", 12))
        text.pack(fill=tk.BOTH, expand=True)
        
        # Format content for display
        raw_content = article.get('summary', '')
        
        if not raw_content or str(raw_content).strip().lower() in ["none", "", "No summary available!"]:
            display_body = (
                "Notice: Content extraction restricted.\n\n"
                "The full content of this article is currently unavailable for direct preview.\n\n"
                "Please click the 'Open in Browser' button to read the complete article."
            )
        else:
            display_body = raw_content
            
        full_content = f"Source: {article['source']}\n"
        full_content += f"URL: {article['url']}\n"
        full_content += "-"*50 + "\n\n"
        full_content += display_body
        
        text.insert("1.0", full_content)
        text.config(state="disabled")



    def show_visualization(self):
            """Display data visualizations."""
    
            if not self.current_article:
                messagebox.showwarning(
                    "No Data",
                    "Please search for news articles first."
                )
                return
    
            visualizer = NewsVisualizer(self.current_article)
    
            visualizer.plot_articles_by_source()
            visualizer.plot_summary_length_by_source()
            visualizer.plot_top_words()

"""News Aggregator package."""

from .components import (
    run_app,
    render_search_controls,
    render_articles,
    render_analytics_panel,
    NewsVisualiser,
    plot_all_categories_trend,
)

__all__ = [
    "run_app",
    "render_search_controls",
    "render_articles",
    "render_analytics_panel",
    "NewsVisualiser",
    "plot_all_categories_trend",
]

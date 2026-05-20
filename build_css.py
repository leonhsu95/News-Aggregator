#!/usr/bin/env python3
"""Build script for compiling CSS stylesheets."""
import sys
from src.styles_loader import compile_css


def main():
    """Compile all stylesheets into a single file."""
    style_files = [
        "styles/header.css",
        "styles/article-display.css",
        "styles/analytics-panel.css"
    ]
    
    print("Building CSS...")
    success = compile_css(style_files, output_file="styles/compiled.css", minify=True)
    
    if success:
        print("Build complete!")
        return 0
    else:
        print("Build failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())

"""Utility module for loading and concatenating CSS stylesheets."""


def load_all_styles(style_files):
    """
    Load and concatenate multiple CSS files into a single string.
    
    Args:
        style_files (list): List of file paths to CSS files
        
    Returns:
        str: Combined CSS content
    """
    combined_css = ""
    for file in style_files:
        try:
            with open(file) as f:
                combined_css += f.read() + "\n"
        except FileNotFoundError:
            print(f"Warning: {file} not found")
    return combined_css

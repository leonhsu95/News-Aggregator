"""Utility module for loading, compiling, and managing CSS stylesheets."""
import os
import re


def minify_css(css_content):
    """
    Minify CSS by removing comments and unnecessary whitespace.
    
    Args:
        css_content (str): Raw CSS content
        
    Returns:
        str: Minified CSS
    """
    # Remove comments
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    # Remove extra whitespace
    css_content = re.sub(r'\s+', ' ', css_content)
    # Remove spaces around special characters
    css_content = re.sub(r'\s*([{}:;,])\s*', r'\1', css_content)
    return css_content.strip()


def load_all_styles(style_files, minify=False):
    """
    Load and concatenate multiple CSS files into a single string.
    
    Args:
        style_files (list): List of file paths to CSS files
        minify (bool): Whether to minify the combined CSS
        
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
    
    if minify:
        combined_css = minify_css(combined_css)
    
    return combined_css


def compile_css(style_files, output_file="styles/compiled.css", minify=True):
    """
    Compile multiple CSS files into a single output file.
    
    Args:
        style_files (list): List of file paths to CSS files
        output_file (str): Path to output compiled CSS file
        minify (bool): Whether to minify the output
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        combined_css = load_all_styles(style_files, minify=minify)
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w') as f:
            f.write(combined_css)
        
        print(f"✓ CSS compiled successfully to {output_file}")
        return True
    except Exception as e:
        print(f"✗ Error compiling CSS: {e}")
        return False

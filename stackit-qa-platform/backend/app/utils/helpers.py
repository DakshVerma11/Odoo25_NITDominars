import bleach
import re
from html.parser import HTMLParser

def sanitize_html(content):
    """
    Sanitize HTML content to prevent XSS attacks while preserving
    allowed formatting elements for the rich text editor
    """
    allowed_tags = [
        'b', 'i', 's', 'u', 'em', 'strong', 'p', 'br', 'hr',
        'ul', 'ol', 'li', 'a', 'img', 'blockquote', 'code', 'pre',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'span'
    ]
    
    allowed_attributes = {
        'a': ['href', 'title', 'target'],
        'img': ['src', 'alt', 'width', 'height'],
        'div': ['class', 'align'],
        'span': ['class', 'style'],
        'p': ['align'],
        'code': ['class'],
        'pre': ['class']
    }
    
    # Sanitize the HTML content
    cleaned_content = bleach.clean(
        content,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True
    )
    
    return cleaned_content

def extract_mentions(content):
    """
    Extract @username mentions from content
    
    Returns:
        List of usernames mentioned
    """
    # Find all @username patterns in the content
    pattern = r'@([a-zA-Z0-9_]{3,})'
    mentions = re.findall(pattern, content)
    
    # Return unique usernames
    return list(set(mentions))

class HTMLStripper(HTMLParser):
    """
    HTML Parser for stripping all HTML tags
    """
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []
        
    def handle_data(self, d):
        self.text.append(d)
        
    def get_text(self):
        return ''.join(self.text)

def strip_html(html):
    """
    Remove all HTML tags from a string
    """
    stripper = HTMLStripper()
    stripper.feed(html)
    return stripper.get_text()

def truncate_text(text, max_length=200):
    """
    Truncate text to specified length adding ellipsis
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length].rsplit(' ', 1)[0] + '...'
import re
from bs4 import BeautifulSoup

def clean_text(text):
    # Use BeautifulSoup to parse and extract the visible text only
    soup = BeautifulSoup(text, 'html.parser')
    
    # Remove JavaScript, CSS, and other non-relevant content
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()  # Remove these tags

    # Get the visible text
    text = soup.get_text()

    # Now apply your additional cleaning
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

    # Remove special characters (leaving only letters, digits, and spaces)
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)

    # Replace multiple spaces with a single space
    text = re.sub(r'\s{2,}', ' ', text)

    # Trim leading and trailing whitespace
    text = text.strip()

    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

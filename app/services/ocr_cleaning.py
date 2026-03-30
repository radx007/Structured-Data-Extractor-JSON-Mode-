import json

from bs4 import BeautifulSoup

def clean_ocr(ocr_item):
    filename = ocr_item.get('filename', 'unknown')
    html_content = ocr_item.get('data', {}).get('ocr', '')
    
    if '<table' not in html_content:
        return f"--- FILE: {filename} (Markdown/Text) ---\n{html_content.strip()}"

    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Replace <br> with spaces so words don't stick together
    for br in soup.find_all("br"):
        br.replace_with(" ")

    lines = []
    for row in soup.find_all('tr'):
        # Get every cell (th or td) regardless of span
        cells = row.find_all(['th', 'td'])
        # Extract text, clean whitespace, and join with a clear separator
        row_text = " || ".join([c.get_text().strip() for c in cells if c.get_text().strip()])
        if row_text:
            lines.append(row_text)
            
    return f"--- FILE: {filename} ---\n" + "\n".join(lines)

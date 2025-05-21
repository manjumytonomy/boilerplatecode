import re
import os

folder = '/Users/vikram/Downloads/Merged_Package'

# Find all matching <meta name="Corresponding English" unique="..." /> tags
pattern = re.compile(r'<meta\s+name="Corresponding [^"<>]+"\s+unique="([^"]+)"\s*/?>\n?', re.IGNORECASE)

def replacer(match):
    key = match.group(1)
    if key in seen:
        return ''
    seen.add(key)
    return match.group(0)

seen = set()
for root, _, files in os.walk(folder):
    for file in files:
        if file.endswith('.html') and file != 'EpicDesktopIndex.html':
            seen = set()
            filepath = os.path.join(root, file)
            with open(filepath) as f:
                html_content = f.read()
            cleaned_html = pattern.sub(replacer, html_content)
            with open(filepath, 'w', encoding="utf-8") as f:
                f.write(cleaned_html)

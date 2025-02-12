import os
import re
from bs4 import BeautifulSoup

# Top-level folder
root_dir = '/Users/Manju/Work/BoilerPlateCodeGitLocal/CorrespondingLanguageScript/HTMLPackage/HTML'

# Recursively walk the directory tree
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            
            # Open and parse HTML file
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                
                # Find meta tag with name="LanguageIndex"
                meta_tag = soup.find('meta', attrs={'name': 'LanguageIndex'})
                
                if meta_tag:
                    content = meta_tag.get('content')
                    
                    # Check suffix and rename meta tag
                    if content.endswith('ES.html'):
                        meta_tag['name'] = 'Corresponding Spanish'
                        content = content.replace('../', '../Spanish/')
                    else:
                        meta_tag['name'] = 'Corresponding English'
                        content = content.replace('../', '../English/')
                    
                    # Update meta tag content
                    meta_tag['content'] = content
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        html_content = f.read()

                    # Reorder attributes
                    html_content = re.sub(r'<meta\s+content="([^"]+)"\s+name="([^"]+)"',
                                        r'<meta name="\2" content="\1"',
                                        html_content)

                    # Save updated HTML file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(html_content)


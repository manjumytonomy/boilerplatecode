import os
from lxml import html

# Top-level folder
root_dir = '/Users/Manju/Mytonomy Inc Dropbox/Manju Komarlu/Written Education - Upwork Share/WE-Tester01/Oct-24-2024-Delivery/HTMLPackage/HTML'

# Recursively walk the directory tree
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            
            # Open and parse HTML file
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = html.parse(f)
                
                # Find meta tags to rename
                meta_tags = tree.xpath('//meta[@name="LanguageIndex"]')
                
                for meta_tag in meta_tags:
                    content = meta_tag.get('content')
                    
                    # Check suffix and rename meta tag
                    if content.endswith('ES.html'):
                        meta_tag.set('name', 'Corresponding Spanish')
                        content = content.replace('../', '../Spanish/')
                    else:
                        meta_tag.set('name', 'Corresponding English')
                        content = content.replace('../', '../English/')
                    
                    # Update meta tag content
                    meta_tag.set('content', content)
                    
                # Remove CorrespondingLanguage meta tags
                corresponding_language_tags = tree.xpath('//meta[@name="CorrespondingLanguage"]')
                for tag in corresponding_language_tags:
                    tag.getparent().remove(tag)
                    
                # Save updated HTML file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(html.tostring(tree, encoding='unicode'))
import os
from lxml import html

def replace_h3_tags(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    tree = html.parse(f)
                
                # Replace h3 tags with p tags
                for h3_tag in tree.xpath('//h3'):
                    h3_tag.tag = 'p'
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(html.tostring(tree, encoding='unicode'))

# Specify top-level directory
directory = '/Users/Manju/Mytonomy Inc Dropbox/Manju Komarlu/Written Education - Upwork Share/WE-Tester01/Oct-30-2024-Delivery - 6. Advocate Aurora Health - Batch 3.3/HTML Package'
replace_h3_tags(directory)


# Key differences from BeautifulSoup:

# 1. html.parse() parses HTML files.
# 2. tree.xpath('//h3') finds all h3 tags using XPath.
# 3. h3_tag.tag = 'p' replaces h3 tags with p tags.
# 4. html.tostring() converts the tree back to HTML.

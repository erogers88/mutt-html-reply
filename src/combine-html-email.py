import sys
from bs4 import BeautifulSoup
import css_inline

# Get filepaths
filepath_msg = sys.argv[1]
filepath_original = sys.argv[2]
filepath_headers = sys.argv[3]

# Open files and get HTML
with open(filepath_msg, 'r') as file:
    html_msg = file.read()
with open(filepath_original, 'r') as file:
    html_original = file.read()
with open(filepath_headers, 'r') as file:
    text_headers = file.read()

# Convert files to BeautifulSoup object and inline all CSS
bs4_msg = BeautifulSoup(css_inline.inline(html_msg),'html.parser')
bs4_original = BeautifulSoup(css_inline.inline(html_original), 'html.parser')

# Parse headers

# Convert headers to HTML

# Combine HTML together

# Write output
with open('/home/erik/temp/html-output.html', 'w') as file:
    html_msg = file.write(str(bs4_original))

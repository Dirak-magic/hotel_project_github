import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
home_html_path = os.path.join(BASE_DIR, 'templates', 'home.html')

with open(home_html_path, 'r', encoding='utf-8') as f:
    home_content = f.read()

# Make it chubby by replacing the text-stroke value
home_content = home_content.replace('-webkit-text-stroke: 2px rgba(255, 255, 255, 0.9);', '-webkit-text-stroke: 4px rgba(255, 255, 255, 0.95);')
home_content = home_content.replace('-webkit-text-stroke: 2px #d4af37;', '-webkit-text-stroke: 4px #d4af37;')

# Make it slightly bigger to accommodate the fatness without losing the hole
home_content = home_content.replace('font-size: clamp(1.8rem, 4vw, 2.8rem);', 'font-size: clamp(2.2rem, 5vw, 3.2rem);')

with open(home_html_path, 'w', encoding='utf-8') as f:
    f.write(home_content)

print("Updated to chubby jelly style successfully!")

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
home_html_path = os.path.join(BASE_DIR, 'templates', 'home.html')

with open(home_html_path, 'r', encoding='utf-8') as f:
    home_content = f.read()

# Expand viewBox to add padding (prevents clipping) and naturally shrinks the icon a bit
home_content = home_content.replace('viewBox="0 0 24 24"', 'viewBox="-4 -4 32 32"')

# Also let's make sure overflow is visible just in case drop-shadow still bleeds
home_content = home_content.replace('class="jelly-chevron"', 'class="jelly-chevron" style="overflow: visible;"')

# The user also wanted to reduce the font-size slightly just to be safe
home_content = home_content.replace('font-size: clamp(2.5rem, 6vw, 4.2rem);', 'font-size: clamp(2rem, 5vw, 3.5rem);')

with open(home_html_path, 'w', encoding='utf-8') as f:
    f.write(home_content)

print("Fixed SVG clipping and reduced size successfully!")

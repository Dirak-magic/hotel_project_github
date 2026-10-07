import re

with open('templates/brand_detail.html', 'r', encoding='utf-8') as f:
    text = f.read()

# The JS block for the timer is at the end of the file.
js_pattern = r'<script>\s*// Countdown Timer JS cho các cơ sở.*?<\/script>'
text = re.sub(js_pattern, '', text, flags=re.DOTALL)

with open('templates/brand_detail.html', 'w', encoding='utf-8') as f:
    f.write(text)

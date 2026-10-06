import re

with open('templates/brand_detail.html', 'r', encoding='utf-8') as f:
    text = f.read()

# The sale block to remove starts with <!-- BANNER KHUYẾN MÃI CỦA CƠ SỞ -->
# and ends with {% endif %} right before <div class="container py-5">
pattern = r'\s*<!-- BANNER KHUYẾN MÃI CỦA CƠ SỞ -->\s*{% if brand\.sale_active %}.*?{% endif %}'

text = re.sub(pattern, '', text, flags=re.DOTALL)

with open('templates/brand_detail.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Removed sale banner from brand_detail')

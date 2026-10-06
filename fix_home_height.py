import re

with open('templates/home.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Revert text style but keep pre-wrap
old_text = '''<div class="mb-5 text-white" style="line-height: 1.8; opacity: 1; font-size: 1.1rem; font-weight: 500; text-shadow: 0 2px 8px rgba(0,0,0,0.9); white-space: pre-wrap;">{{ prop.sale_description }}</div>'''
new_text = '''<div class="mb-5 text-light" style="line-height: 2; opacity: 0.8; font-size: 1.05rem; font-weight: 300; white-space: pre-wrap;">{{ prop.sale_description }}</div>'''
text = text.replace(old_text, new_text)

# 2. Fix height issue
# The current container has: <div class="container py-5 d-flex align-items-center" style="min-height: 70vh;">
# And the parent sale-section has: <div class="container-fluid position-relative sale-section p-0" style="...">
# I will make the sale-section fixed height, and container 100% height.

# Let's find the sale-section and modify its style
# The string is long, so I'll use regex to target it.
pattern = r'(<div class="container-fluid position-relative sale-section p-0" style="[^"]+)(")'
text = re.sub(pattern, r'\1; height: 85vh; min-height: 750px;\2', text)

# Then change the inner container to height: 100% instead of min-height: 70vh
text = text.replace(
    '<div class="container py-5 d-flex align-items-center" style="min-height: 70vh;">',
    '<div class="container py-4 d-flex align-items-center h-100">'
)

with open('templates/home.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated text style and fixed height')

import re

with open('templates/home.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Height and vertical center
text = text.replace(
    '<div class="container py-5" style="min-height: 500px;">',
    '<div class="container py-5 d-flex align-items-center" style="min-height: 70vh;">'
)

# 2. Text styling and pre-wrap
old_text_block = '''                            <div class="mb-5 text-light" style="line-height: 2; opacity: 0.8; font-size: 1.05rem; font-weight: 300;">
                                {{ prop.sale_description|linebreaksbr }}
                            </div>'''

new_text_block = '''                            <div class="mb-5 text-white" style="line-height: 1.8; opacity: 1; font-size: 1.1rem; font-weight: 500; text-shadow: 0 2px 8px rgba(0,0,0,0.9); white-space: pre-wrap;">{{ prop.sale_description }}</div>'''

if old_text_block in text:
    text = text.replace(old_text_block, new_text_block)
else:
    # try regex just in case
    text = re.sub(
        r'<div class="mb-5 text-light" style="[^"]*">\s*{{ prop\.sale_description\|linebreaksbr }}\s*</div>',
        new_text_block,
        text
    )

with open('templates/home.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated sale description and height')

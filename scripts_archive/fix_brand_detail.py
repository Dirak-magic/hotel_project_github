import re

with open('templates/brand_detail.html', 'r', encoding='utf-8') as f:
    text = f.read()

broken_pattern = r'(role="tabpanel">)" class="card-img".*?(?=<!-- Danh sách Hạng phòng)'

text = re.sub(broken_pattern, r'\1\n\n            ', text, flags=re.DOTALL)

with open('templates/brand_detail.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Fixed broken HTML')

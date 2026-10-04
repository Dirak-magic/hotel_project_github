import re

with open('core/urls.py', 'r', encoding='utf-8') as f:
    text = f.read()

if "'contact'" not in text:
    text = text.replace("]", "    path('lien-he/', views.contact_view, name='contact'),\n]")

with open('core/urls.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Added contact URL")

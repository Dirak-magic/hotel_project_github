import re

with open('templates/home.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    '<div class="row align-items-center justify-content-between my-5">',
    '<div class="row align-items-center justify-content-between my-5 w-100 m-0">'
)

with open('templates/home.html', 'w', encoding='utf-8') as f:
    f.write(text)


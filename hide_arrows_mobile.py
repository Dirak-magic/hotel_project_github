import re

with open('templates/home.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    '<button class="carousel-control-prev luxury-control" type="button"',
    '<button class="carousel-control-prev luxury-control d-none d-md-flex" type="button"'
)
text = text.replace(
    '<button class="carousel-control-next luxury-control" type="button"',
    '<button class="carousel-control-next luxury-control d-none d-md-flex" type="button"'
)

with open('templates/home.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Hidden arrows on mobile')

import re

with open('templates/home.html', 'r', encoding='utf-8') as f:
    text = f.read()

custom_css = '''
    .carousel-control-prev-icon,
    .carousel-control-next-icon {
        width: 3rem;
        height: 3rem;
        background-color: rgba(0, 0, 0, 0.5);
        border-radius: 50%;
        background-size: 50%;
    }
    .carousel-indicators [data-bs-target] {
        width: 40px;
        height: 6px;
        border-radius: 3px;
        background-color: rgba(255, 255, 255, 0.5);
    }
    .carousel-indicators .active {
        background-color: #d4af37;
    }
'''

text = text.replace('</style>', custom_css + '</style>')

with open('templates/home.html', 'w', encoding='utf-8') as f:
    f.write(text)


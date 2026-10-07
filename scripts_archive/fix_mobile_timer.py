import re

with open('templates/home.html', 'r', encoding='utf-8') as f:
    text = f.read()

mobile_css = '''
    @media (max-width: 576px) {
        .luxury-timer-box {
            width: 70px !important;
            padding: 1rem 0.2rem !important;
        }
        .luxury-timer-box .display-5 {
            font-size: 1.8rem !important;
        }
        .luxury-timer-box .small {
            font-size: 0.6rem !important;
            letter-spacing: 1px !important;
        }
        .sale-countdown-timer {
            gap: 0.5rem !important;
            justify-content: center !important;
            width: 100%;
        }
    }
'''

text = text.replace('</style>', mobile_css + '\n</style>')

with open('templates/home.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Added mobile CSS for timer')

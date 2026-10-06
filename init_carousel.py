import re

with open('templates/home.html', 'r', encoding='utf-8') as f:
    text = f.read()

js_init = '''
    // Force start the carousel
    document.addEventListener("DOMContentLoaded", function() {
        var myCarousel = document.querySelector('#saleCarousel');
        if (myCarousel) {
            var carousel = new bootstrap.Carousel(myCarousel, {
                interval: 4000,
                ride: 'carousel'
            });
            carousel.cycle();
        }
    });
'''

# insert before the Countdown JS
text = text.replace('// Countdown Timer JS (Multiple)', js_init + '\n    // Countdown Timer JS (Multiple)')

with open('templates/home.html', 'w', encoding='utf-8') as f:
    f.write(text)

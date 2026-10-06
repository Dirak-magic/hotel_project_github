import re

with open('templates/home.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace Indicators
old_indicators = '''    <!-- Indicators -->
    <div class="carousel-indicators" style="bottom: 120px;">
        {% for prop in sale_properties %}
        <button type="button" data-bs-target="#saleCarousel" data-bs-slide-to="{{ forloop.counter0 }}" {% if forloop.first %}class="active"{% endif %} aria-label="Slide {{ forloop.counter }}"></button>
        {% endfor %}
    </div>'''

new_indicators = '''    <!-- Indicators (Luxury Edition) -->
    <div class="carousel-indicators luxury-indicators">
        {% for prop in sale_properties %}
        <button type="button" data-bs-target="#saleCarousel" data-bs-slide-to="{{ forloop.counter0 }}" {% if forloop.first %}class="active"{% endif %} aria-label="Slide {{ forloop.counter }}"></button>
        {% endfor %}
    </div>'''

text = text.replace(old_indicators, new_indicators)

# Replace Controls
old_controls = '''    <!-- Controls -->
    {% if sale_properties|length > 1 %}
    <button class="carousel-control-prev" type="button" data-bs-target="#saleCarousel" data-bs-slide="prev" style="width: 5%;">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-target="#saleCarousel" data-bs-slide="next" style="width: 5%;">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
    </button>
    {% endif %}'''

new_controls = '''    <!-- Controls (Luxury Edition) -->
    {% if sale_properties|length > 1 %}
    <button class="carousel-control-prev luxury-control" type="button" data-bs-target="#saleCarousel" data-bs-slide="prev">
        <div class="control-circle">
            <i class="bi bi-chevron-left"></i>
        </div>
        <span class="visually-hidden">Previous</span>
    </button>
    <button class="carousel-control-next luxury-control" type="button" data-bs-target="#saleCarousel" data-bs-slide="next">
        <div class="control-circle">
            <i class="bi bi-chevron-right"></i>
        </div>
        <span class="visually-hidden">Next</span>
    </button>
    {% endif %}'''

text = text.replace(old_controls, new_controls)

# Now, add the CSS. I'll replace my old custom CSS with the new one.
old_css_start = '    .carousel-control-prev-icon,'
old_css_end = '    .carousel-indicators .active {\n        background-color: #d4af37;\n    }'

# If it exists, remove the old CSS block
if old_css_start in text:
    start_idx = text.find(old_css_start)
    end_idx = text.find(old_css_end) + len(old_css_end)
    text = text[:start_idx] + text[end_idx:]

# Add new CSS
luxury_css = '''
    /* LUXURY CAROUSEL CONTROLS & INDICATORS */
    .luxury-control {
        width: 8%;
        opacity: 0.8;
        transition: all 0.4s ease;
    }
    .luxury-control:hover {
        opacity: 1;
    }
    .control-circle {
        width: 60px;
        height: 60px;
        background-color: rgba(15, 15, 15, 0.6);
        border: 2px solid rgba(212, 175, 55, 0.5); /* Gold border */
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #d4af37; /* Gold icon */
        font-size: 1.8rem;
        backdrop-filter: blur(5px);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 0 15px rgba(0,0,0,0.5);
    }
    .luxury-control:hover .control-circle {
        background-color: rgba(212, 175, 55, 0.9);
        border-color: #fce38a;
        color: #111;
        transform: scale(1.15);
        box-shadow: 0 0 25px rgba(212, 175, 55, 0.6);
    }

    .luxury-indicators {
        bottom: 120px;
        gap: 12px;
    }
    .luxury-indicators [data-bs-target] {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background-color: transparent;
        border: 2px solid rgba(212, 175, 55, 0.6);
        opacity: 0.7;
        transition: all 0.4s ease;
        margin: 0;
        box-sizing: border-box;
    }
    .luxury-indicators .active {
        background-color: #d4af37;
        border-color: #d4af37;
        transform: scale(1.4);
        opacity: 1;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.8);
    }
    .luxury-indicators [data-bs-target]:hover {
        opacity: 1;
        border-color: #fce38a;
        transform: scale(1.2);
    }
'''

text = text.replace('</style>', luxury_css + '\n</style>')

with open('templates/home.html', 'w', encoding='utf-8') as f:
    f.write(text)

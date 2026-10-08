import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
home_html_path = os.path.join(BASE_DIR, 'templates', 'home.html')

with open(home_html_path, 'r', encoding='utf-8') as f:
    home_content = f.read()

# Replace left icon
old_left_icon = '<i class="bi bi-chevron-left"></i>'
new_left_icon = '''<svg viewBox="0 0 24 24" class="jelly-chevron" xmlns="http://www.w3.org/2000/svg">
                <path d="M15.5 3.5a2.5 2.5 0 0 0-3.54 0L3.5 11.96a2.5 2.5 0 0 0 0 3.54l8.46 8.46a2.5 2.5 0 0 0 3.54-3.54L8.04 13.46l7.46-7.46a2.5 2.5 0 0 0 0-3.54z" />
            </svg>'''
home_content = home_content.replace(old_left_icon, new_left_icon)

# Replace right icon
old_right_icon = '<i class="bi bi-chevron-right"></i>'
new_right_icon = '''<svg viewBox="0 0 24 24" class="jelly-chevron" xmlns="http://www.w3.org/2000/svg">
                <path d="M8.5 3.5a2.5 2.5 0 0 1 3.54 0l8.46 8.46a2.5 2.5 0 0 1 0 3.54l-8.46 8.46a2.5 2.5 0 0 1-3.54-3.54l7.46-7.46-7.46-7.46a2.5 2.5 0 0 1 0-3.54z" />
            </svg>'''
home_content = home_content.replace(old_right_icon, new_right_icon)

# Update CSS to target SVG
css_pattern = r'\.control-circle\s*\{[^}]*\}'
new_css = """.control-circle {
        background: transparent;
        border: none;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 0;
        width: auto;
        height: auto;
        padding: 20px;
        
        font-size: clamp(2.5rem, 6vw, 4.2rem);
        filter: drop-shadow(0px 8px 10px rgba(0, 0, 0, 0.40));
        transition: all 0.4s ease;
    }
    .jelly-chevron {
        width: 1em;
        height: 1em;
        fill: rgba(255, 255, 255, 0.72);
        stroke: rgba(255, 255, 255, 0.45);
        stroke-width: 1.5px;
        stroke-linejoin: round;
        transition: all 0.4s ease;
    }"""
home_content = re.sub(css_pattern, new_css, home_content)

hover_pattern = r'\.luxury-control:hover\s*\.control-circle\s*\{[^}]*\}'
new_hover = """.luxury-control:hover .control-circle {
        background: transparent;
        border: none;
        transform: scale(1.06);
        filter: drop-shadow(0px 10px 15px rgba(0, 0, 0, 0.50)) drop-shadow(0px 0px 25px rgba(212, 175, 55, 0.65));
    }
    .luxury-control:hover .jelly-chevron {
        fill: rgba(212, 175, 55, 0.75);
        stroke: rgba(212, 175, 55, 0.45);
    }"""
home_content = re.sub(hover_pattern, new_hover, home_content)

with open(home_html_path, 'w', encoding='utf-8') as f:
    f.write(home_content)

print("Updated HTML and CSS to use actual SVG Jelly Chevrons!")

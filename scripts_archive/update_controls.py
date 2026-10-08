import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
home_html_path = os.path.join(BASE_DIR, 'templates', 'home.html')

with open(home_html_path, 'r', encoding='utf-8') as f:
    home_content = f.read()

# 1. Update button classes (remove d-none)
home_content = home_content.replace('luxury-control d-none d-md-flex', 'luxury-control d-flex')

# 2. Update CSS for .control-circle using regex to catch all instances
# Replace .control-circle { ... }
control_circle_pattern = r'\.control-circle\s*\{[^}]*\}'
new_control_circle = """.control-circle {
        width: clamp(40px, 8vw, 70px);
        height: clamp(40px, 8vw, 70px);
        background-color: transparent;
        border: 1px solid transparent;
        border-radius: 5px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: rgba(212, 175, 55, 0.7);
        font-size: clamp(2rem, 5vw, 3.5rem);
        font-weight: 300;
        transition: all 0.4s ease;
        box-shadow: none;
        backdrop-filter: none;
    }"""
home_content = re.sub(control_circle_pattern, new_control_circle, home_content)

# Replace .luxury-control:hover .control-circle { ... }
hover_pattern = r'\.luxury-control:hover\s*\.control-circle\s*\{[^}]*\}'
new_hover = """.luxury-control:hover .control-circle {
        background-color: rgba(15, 15, 15, 0.2);
        border: 1px solid rgba(212, 175, 55, 0.8);
        color: #d4af37;
        transform: scale(1.1);
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.3);
        backdrop-filter: blur(3px);
    }"""
home_content = re.sub(hover_pattern, new_hover, home_content)

with open(home_html_path, 'w', encoding='utf-8') as f:
    f.write(home_content)

print("Updated carousel controls successfully!")

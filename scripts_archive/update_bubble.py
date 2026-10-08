import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
home_html_path = os.path.join(BASE_DIR, 'templates', 'home.html')

with open(home_html_path, 'r', encoding='utf-8') as f:
    home_content = f.read()

# Replace .control-circle { ... }
control_circle_pattern = r'\.control-circle\s*\{[^}]*\}'
new_control_circle = """.control-circle {
        width: clamp(40px, 8vw, 65px);
        height: clamp(40px, 8vw, 65px);
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #F4F0E8;
        font-size: clamp(1.2rem, 3vw, 2rem);
        transition: all 0.4s ease;
        box-shadow: inset 0 0 10px rgba(255,255,255,0.1), 0 5px 15px rgba(0,0,0,0.3);
        backdrop-filter: blur(8px);
    }"""
home_content = re.sub(control_circle_pattern, new_control_circle, home_content)

# Replace .luxury-control:hover .control-circle { ... }
hover_pattern = r'\.luxury-control:hover\s*\.control-circle\s*\{[^}]*\}'
new_hover = """.luxury-control:hover .control-circle {
        background-color: rgba(212, 175, 55, 0.15);
        border: 1px solid rgba(212, 175, 55, 0.6);
        color: #fce38a;
        transform: scale(1.15);
        box-shadow: inset 0 0 20px rgba(212,175,55,0.2), 0 8px 20px rgba(0,0,0,0.4);
        backdrop-filter: blur(10px);
    }"""
home_content = re.sub(hover_pattern, new_hover, home_content)

with open(home_html_path, 'w', encoding='utf-8') as f:
    f.write(home_content)

print("Updated to bubble style successfully!")

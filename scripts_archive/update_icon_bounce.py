import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
home_html_path = os.path.join(BASE_DIR, 'templates', 'home.html')

with open(home_html_path, 'r', encoding='utf-8') as f:
    home_content = f.read()

# Replace .control-circle { ... }
control_circle_pattern = r'\.control-circle\s*\{[^}]*\}'
new_control_circle = """.control-circle {
        background: transparent;
        border: none;
        display: flex;
        align-items: center;
        justify-content: center;
        color: rgba(255, 255, 255, 0.6);
        font-size: clamp(1.5rem, 3.5vw, 2.5rem);
        transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: none;
        backdrop-filter: none;
        border-radius: 0;
        width: auto;
        height: auto;
        padding: 20px;
    }"""
home_content = re.sub(control_circle_pattern, new_control_circle, home_content)

# Replace .luxury-control:hover .control-circle { ... }
hover_pattern = r'\.luxury-control:hover\s*\.control-circle\s*\{[^}]*\}'
new_hover = """.luxury-control:hover .control-circle {
        background: transparent;
        border: none;
        color: #d4af37;
        transform: scale(1.8);
        text-shadow: 0 0 15px rgba(212, 175, 55, 0.8);
        box-shadow: none;
        backdrop-filter: none;
    }"""
home_content = re.sub(hover_pattern, new_hover, home_content)

with open(home_html_path, 'w', encoding='utf-8') as f:
    f.write(home_content)

print("Updated icon to bouncy small style!")

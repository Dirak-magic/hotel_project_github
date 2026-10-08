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
        border-radius: 0;
        width: auto;
        height: auto;
        padding: 20px;
        
        /* JELLY BUBBLE CHEVRON SPECS */
        font-size: clamp(2.5rem, 6vw, 4.2rem);
        color: rgba(255, 255, 255, 0.72);
        -webkit-text-stroke: 2px rgba(255, 255, 255, 0.45);
        filter: drop-shadow(0px 8px 10px rgba(0, 0, 0, 0.40));
        
        transition: all 0.4s ease;
    }"""
home_content = re.sub(control_circle_pattern, new_control_circle, home_content)

# Replace .luxury-control:hover .control-circle { ... }
hover_pattern = r'\.luxury-control:hover\s*\.control-circle\s*\{[^}]*\}'
new_hover = """.luxury-control:hover .control-circle {
        background: transparent;
        border: none;
        
        /* JELLY BUBBLE HOVER SPECS */
        color: rgba(212, 175, 55, 0.75);
        -webkit-text-stroke: 2px rgba(212, 175, 55, 0.45);
        transform: scale(1.06);
        filter: drop-shadow(0px 10px 15px rgba(0, 0, 0, 0.50)) drop-shadow(0px 0px 25px rgba(212, 175, 55, 0.65));
    }"""
home_content = re.sub(hover_pattern, new_hover, home_content)

with open(home_html_path, 'w', encoding='utf-8') as f:
    f.write(home_content)

print("Updated to exact Jelly Bubble specs successfully!")

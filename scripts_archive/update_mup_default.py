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
        
        /* LIQUID BUBBLE STYLE (Mặc định to và múp) */
        color: #ffffff;
        -webkit-text-stroke: 12px rgba(255, 255, 255, 0.25);
        
        font-size: clamp(2.5rem, 6vw, 4.2rem); /* Đã phóng to gấp rưỡi */
        
        filter: drop-shadow(0px 8px 10px rgba(0,0,0,0.4)) drop-shadow(inset 0px 5px 15px rgba(255,255,255,0.6));
        
        transition: all 0.4s ease; /* Chuyển màu mượt mà */
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
        
        /* HOVER: Chỉ đổi màu Vàng Luxury, KHÔNG phóng to */
        color: #ffffff;
        -webkit-text-stroke: 12px rgba(212, 175, 55, 0.65);
        
        filter: drop-shadow(0px 10px 15px rgba(0,0,0,0.5)) drop-shadow(0px 0px 25px rgba(212, 175, 55, 0.8));
    }"""
home_content = re.sub(hover_pattern, new_hover, home_content)

with open(home_html_path, 'w', encoding='utf-8') as f:
    f.write(home_content)

print("Updated to Mup Default style successfully!")

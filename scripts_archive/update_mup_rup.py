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
        
        /* LIQUID BUBBLE STYLE (Icon #3) */
        color: #ffffff; /* Lõi mũi tên màu trắng đặc */
        -webkit-text-stroke: 10px rgba(255, 255, 255, 0.25); /* Tạo lớp bọc nước dày và trong suốt */
        
        font-size: clamp(1.8rem, 4vw, 2.8rem);
        
        /* Phủ thêm bóng phản quang 3D để cục nước bóng bẩy hơn */
        filter: drop-shadow(0px 8px 10px rgba(0,0,0,0.4)) drop-shadow(inset 0px 5px 15px rgba(255,255,255,0.6));
        
        transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
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
        
        /* HOVER: Múp rụp, căng phồng và hóa Vàng Luxury */
        color: #ffffff; /* Lõi vẫn trắng sáng */
        -webkit-text-stroke: 12px rgba(212, 175, 55, 0.65); /* Lớp bọc nước hóa vàng rực và dày hơn tí */
        transform: scale(1.6);
        
        /* Ánh sáng vàng mờ tỏa ra lung linh */
        filter: drop-shadow(0px 10px 15px rgba(0,0,0,0.5)) drop-shadow(0px 0px 25px rgba(212, 175, 55, 0.8));
    }"""
home_content = re.sub(hover_pattern, new_hover, home_content)

with open(home_html_path, 'w', encoding='utf-8') as f:
    f.write(home_content)

print("Updated to Liquid Bubble Mup Rup style successfully!")

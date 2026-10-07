import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Update base.html to include Google Fonts
base_html_path = os.path.join(BASE_DIR, 'templates', 'base.html')
with open(base_html_path, 'r', encoding='utf-8') as f:
    base_content = f.read()

font_link = '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Montserrat:wght@400;500;600&display=swap" rel="stylesheet">'
if 'Cormorant+Garamond' not in base_content:
    base_content = base_content.replace(
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons',
        font_link + '\n    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons'
    )
    with open(base_html_path, 'w', encoding='utf-8') as f:
        f.write(base_content)

# 2. Update home.html
home_html_path = os.path.join(BASE_DIR, 'templates', 'home.html')
with open(home_html_path, 'r', encoding='utf-8') as f:
    home_content = f.read()

# Update Background gradient & image
home_content = home_content.replace(
    "linear-gradient(rgba(15, 15, 15, 0.75), rgba(15, 15, 15, 0.85))",
    "linear-gradient(to right, rgba(15, 15, 15, 0.95) 0%, rgba(15, 15, 15, 0.7) 40%, rgba(15, 15, 15, 0.1) 100%)"
)
home_content = home_content.replace(
    "https://images.unsplash.com/photo-1571896349842-33c89424de2d?q=80&w=2000&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1566073771259-6a8506099945?q=80&w=2000&auto=format&fit=crop"
)

# Update Subtitle (Đặc Quyền Tại...)
old_subtitle = 'style="letter-spacing: 4px; color: #d4af37; font-size: 0.85rem; border-bottom: 1px solid #d4af37; padding-bottom: 6px; font-weight: 800; color: #fce38a;"'
new_subtitle = 'style="letter-spacing: 3px; color: #D4AF37; font-size: 17px; font-family: \'Montserrat\', sans-serif; border-bottom: 1px solid rgba(212, 175, 55, 0.5); padding-bottom: 6px; font-weight: 600;"'
home_content = home_content.replace(old_subtitle, new_subtitle)

# Update Title
old_title = 'style="color: #ffffff; font-family: \'Playfair Display\', serif; letter-spacing: 1px; line-height: 1.3; white-space: nowrap; font-size: clamp(1.2rem, 2.5vw, 2.3rem);"'
new_title = 'style="color: #F4F0E8; font-family: \'Cormorant Garamond\', serif; font-weight: 600; letter-spacing: 1px; line-height: 1.3; white-space: nowrap; font-size: clamp(1.2rem, 2.5vw, 2.3rem);"'
home_content = home_content.replace(old_title, new_title)

# Update Description
old_desc = 'class="mb-5 text-light" style="line-height: 2; opacity: 0.8; font-size: 1.05rem; font-weight: 300; white-space: pre-wrap;"'
new_desc = 'class="mb-5 sale-desc-content" style="color: #D6D1C8; font-family: \'Montserrat\', sans-serif; font-size: 15px; line-height: 1.9; font-weight: 400; white-space: pre-wrap;"'
home_content = home_content.replace(old_desc, new_desc)

# Update JS Countdown Numbers
old_num = 'class="display-5 fw-bold" style="color: #ffffff; text-shadow: 0 0 10px rgba(255,255,255,0.3); font-family: \'Playfair Display\', serif;"'
new_num = 'style="color: #F4F0E8; font-family: \'Cormorant Garamond\', serif; font-size: 50px; font-weight: 600;"'
home_content = home_content.replace(old_num, new_num)
home_content = home_content.replace('class="display-5 fw-bold" style="color: #F4F0E8;', 'style="color: #F4F0E8;')

# Update JS Countdown Labels
old_label = 'class="small text-uppercase mt-2" style="color: #d4af37; letter-spacing: 2px; font-weight: 600; font-size: 0.7rem;"'
new_label = 'class="small text-uppercase mt-2" style="color: #D4AF37; font-family: \'Montserrat\', sans-serif; letter-spacing: 2px; font-weight: 600; font-size: 11px;"'
home_content = home_content.replace(old_label, new_label)

# Add JS highlight logic at the end of file before {% endblock %}
js_highlight = """
<script>
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.sale-desc-content').forEach(function(el) {
        let html = el.innerHTML;
        // Split by newlines and wrap lines starting with **
        let lines = html.split('\\n');
        for(let i=0; i<lines.length; i++) {
            if(lines[i].trim().startsWith('**')) {
                lines[i] = '<span style="color: #D4AF37; font-weight: 600;">' + lines[i] + '</span>';
            }
        }
        el.innerHTML = lines.join('\\n');
    });
});
</script>
"""
if "sale-desc-content" not in home_content or "split('\\n')" not in home_content:
    home_content = home_content.replace('{% endblock %}', js_highlight + '\n{% endblock %}')

with open(home_html_path, 'w', encoding='utf-8') as f:
    f.write(home_content)

print("Done updating styles!")

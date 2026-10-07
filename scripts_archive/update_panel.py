import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
home_html_path = os.path.join(BASE_DIR, 'templates', 'home.html')

with open(home_html_path, 'r', encoding='utf-8') as f:
    home_content = f.read()

old_left_col = """                        <!-- Cột trái: Nội dung -->
                        <div class="col-lg-6 text-white mb-5 mb-lg-0 pe-lg-5">
                            <div class="mb-4">
                                <span class="text-uppercase" style="letter-spacing: 3px; color: #D4AF37; font-size: 17px; font-family: 'Montserrat', sans-serif; border-bottom: 1px solid rgba(212, 175, 55, 0.5); padding-bottom: 6px; font-weight: 600;">Đặc Quyền Tại {{ prop.name }}</span>
                            </div>
                            
                            <h2 class="mb-4" style="color: #F4F0E8; font-family: 'Cormorant Garamond', serif; font-weight: 600; letter-spacing: 1px; line-height: 1.3; white-space: nowrap; font-size: clamp(1.2rem, 2.5vw, 2.3rem);">{{ prop.sale_title }}</h2>
                            
                            <div class="mb-5 sale-desc-content" style="color: #D6D1C8; font-family: 'Montserrat', sans-serif; font-size: 15px; line-height: 1.9; font-weight: 400; white-space: pre-wrap;">{{ prop.sale_description }}</div>
                            
                            {% if prop.sale_button_link %}
                            <a href="{{ prop.sale_button_link }}" target="_blank" class="btn luxury-btn px-5 py-3 text-uppercase fw-semibold" style="letter-spacing: 2px; font-size: 0.85rem; transition: all 0.4s ease;">
                                {{ prop.sale_button_text }}
                            </a>
                            {% endif %}
                        </div>"""

new_left_col = """                        <!-- Cột trái: Nội dung -->
                        <div class="col-lg-6 text-white mb-5 mb-lg-0 pe-lg-5">
                            <!-- Luxury Content Panel -->
                            <div class="p-4 p-lg-5" style="background: rgba(0, 0, 0, 0.25); backdrop-filter: blur(6px); border: 1px solid rgba(212, 175, 55, 0.2); border-radius: 2px; box-shadow: 0 10px 30px rgba(0,0,0,0.15);">
                                <div class="mb-4">
                                    <span class="text-uppercase" style="letter-spacing: 3px; color: #D4AF37; font-size: 17px; font-family: 'Montserrat', sans-serif; border-bottom: 1px solid rgba(212, 175, 55, 0.5); padding-bottom: 6px; font-weight: 600;">Đặc Quyền Tại {{ prop.name }}</span>
                                </div>
                                
                                <h2 class="mb-4" style="color: #F4F0E8; font-family: 'Cormorant Garamond', serif; font-weight: 600; letter-spacing: 1px; line-height: 1.3; white-space: nowrap; font-size: clamp(1.2rem, 2.5vw, 2.3rem);">{{ prop.sale_title }}</h2>
                                
                                <div class="mb-5 sale-desc-content" style="color: #D6D1C8; font-family: 'Montserrat', sans-serif; font-size: 15px; line-height: 1.9; font-weight: 400; white-space: pre-wrap;">{{ prop.sale_description }}</div>
                                
                                {% if prop.sale_button_link %}
                                <a href="{{ prop.sale_button_link }}" target="_blank" class="btn luxury-btn px-5 py-3 text-uppercase fw-semibold" style="letter-spacing: 2px; font-size: 0.85rem; transition: all 0.4s ease;">
                                    {{ prop.sale_button_text }}
                                </a>
                                {% endif %}
                            </div>
                        </div>"""

if old_left_col in home_content:
    home_content = home_content.replace(old_left_col, new_left_col)
    with open(home_html_path, 'w', encoding='utf-8') as f:
        f.write(home_content)
    print("Updated panel successfully!")
else:
    print("Could not find the block to replace!")

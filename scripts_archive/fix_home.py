import re
with open('templates/home.html', 'r', encoding='utf-8') as f:
    text = f.read()

# We want to replace from {% if sale_properties %} down to {% else %}\n    <!-- NẾU KHÔNG CÓ SALE SECTION
start_idx = text.find('{% if sale_properties %}')
end_idx = text.find('{% else %}\n    <!-- NẾU KHÔNG CÓ SALE SECTION')

if start_idx != -1 and end_idx != -1:
    new_sale_start = '''{% if sale_properties %}
<!-- BỘ BANNER KHUYẾN MÃI (LUXURY EDITION) -->
<div id="saleCarousel" class="carousel slide carousel-fade" data-bs-ride="carousel" data-bs-interval="5000">
    <!-- Indicators -->
    <div class="carousel-indicators" style="bottom: 120px;">
        {% for prop in sale_properties %}
        <button type="button" data-bs-target="#saleCarousel" data-bs-slide-to="{{ forloop.counter0 }}" {% if forloop.first %}class="active"{% endif %} aria-label="Slide {{ forloop.counter }}"></button>
        {% endfor %}
    </div>

    <div class="carousel-inner">
        {% for prop in sale_properties %}
        <div class="carousel-item {% if forloop.first %}active{% endif %}">
            <div class="container-fluid position-relative sale-section p-0" style="background-image: linear-gradient(rgba(15, 15, 15, 0.75), rgba(15, 15, 15, 0.85)), url('{% if prop.sale_background %}{{ prop.sale_background.url }}{% else %}https://images.unsplash.com/photo-1571896349842-33c89424de2d?q=80&w=2000&auto=format&fit=crop{% endif %}'); background-size: cover; background-position: center; box-shadow: 0 15px 40px rgba(0,0,0,0.6);">
                <div class="container py-5" style="min-height: 500px;">
                    <div class="row align-items-center justify-content-between my-5">
                        
                        <!-- Cột trái: Nội dung -->
                        <div class="col-lg-6 text-white mb-5 mb-lg-0 pe-lg-5">
                            <div class="mb-4">
                                <span class="text-uppercase" style="letter-spacing: 4px; color: #d4af37; font-size: 0.85rem; border-bottom: 1px solid #d4af37; padding-bottom: 6px; font-weight: 800; color: #fce38a;">Đặc Quyền Tại {{ prop.name }}</span>
                            </div>
                            
                            <h2 class="display-4 mb-4" style="color: #ffffff; font-family: 'Playfair Display', serif; letter-spacing: 2px; line-height: 1.3;">{{ prop.sale_title }}</h2>
                            
                            <div class="mb-5 text-light" style="line-height: 2; opacity: 0.8; font-size: 1.05rem; font-weight: 300;">
                                {{ prop.sale_description|linebreaksbr }}
                            </div>
                            
                            {% if prop.sale_button_link %}
                            <a href="{{ prop.sale_button_link }}" target="_blank" class="btn luxury-btn px-5 py-3 text-uppercase fw-semibold" style="letter-spacing: 2px; font-size: 0.85rem; transition: all 0.4s ease;">
                                {{ prop.sale_button_text }}
                            </a>
                            {% endif %}
                        </div>
                        
                        <!-- Cột phải: Đếm ngược -->
                        <div class="col-lg-5">
                            <div class="d-flex flex-wrap justify-content-lg-end gap-3 countdown-wrapper sale-countdown-timer" data-endtime="{{ prop.sale_end_date|date:'c' }}">
                                <!-- Sẽ được điền bằng Javascript -->
                            </div>
                        </div>
                        
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>

    <!-- Controls -->
    {% if sale_properties|length > 1 %}
    <button class="carousel-control-prev" type="button" data-bs-target="#saleCarousel" data-bs-slide="prev" style="width: 5%;">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-target="#saleCarousel" data-bs-slide="next" style="width: 5%;">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
    </button>
    {% endif %}

    <!-- Dải Icon Tiện Ích Toàn Cầu (Đưa ra khỏi carousel-inner để giữ cố định bên dưới) -->
    <div class="container-fluid py-5 bg-transparent border-0 position-relative" style="border-top: 1px solid rgba(255,255,255,0.05) !important; margin-top: -100px; z-index: 10;">
        <div class="container">
            <div class="row g-4 text-center">
                <div class="col-6 col-md-3 amenity-item">
                    <i class="bi bi-wifi luxury-icon"></i>
                    <h6 class="text-uppercase luxury-text mt-3 mb-0">Free WiFi</h6>
                </div>
                <div class="col-6 col-md-3 amenity-item">
                    <i class="bi bi-p-circle luxury-icon"></i>
                    <h6 class="text-uppercase luxury-text mt-3 mb-0">Secure Parking</h6>
                </div>
                <div class="col-6 col-md-3 amenity-item">
                    <i class="bi bi-cup-hot luxury-icon"></i>
                    <h6 class="text-uppercase luxury-text mt-3 mb-0">Coffee & Cinebar</h6>
                </div>
                <div class="col-6 col-md-3 amenity-item">
                    <i class="bi bi-bell luxury-icon"></i>
                    <h6 class="text-uppercase luxury-text mt-3 mb-0">Room Service</h6>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .luxury-btn {
        background-color: transparent;
        color: #d4af37;
        border: 1px solid #d4af37;
        border-radius: 0;
    }
    .luxury-btn:hover {
        background-color: #d4af37;
        color: #111;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
    }
    .luxury-timer-box {
        padding: 1.5rem 1rem;
        width: 105px;
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(212, 175, 55, 0.25);
        border-radius: 8px;
        backdrop-filter: blur(15px);
        transition: all 0.4s ease;
    }
    .luxury-timer-box:hover {
        border-color: rgba(212, 175, 55, 0.7);
        transform: translateY(-8px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.6);
    }
</style>
'''
    text = text[:start_idx] + new_sale_start + text[end_idx:]
    with open('templates/home.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed home.html")
else:
    print("Could not find start or end index")

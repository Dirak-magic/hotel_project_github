import re
with open('templates/home.html', 'r', encoding='utf-8') as f:
    html = f.read()

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
</style>'''

start_idx = html.find('{% if site_setting.sale_active %}')
end_idx = html.find('{% else %}', start_idx)

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + new_sale_start + html[end_idx:]

    # Now let's fix the javascript that queries #sale-countdown
    js_old = '''    // Countdown Timer JS (Restored)
    document.addEventListener("DOMContentLoaded", function() {
        const timerContainer = document.getElementById('sale-countdown');
        if (timerContainer) {
            const endDateStr = timerContainer.getAttribute('data-endtime');
            if (endDateStr) {
                const endDate = new Date(endDateStr).getTime();
                
                const timerInterval = setInterval(function() {
                    const now = new Date().getTime();
                    const distance = endDate - now;
                    
                    if (distance < 0) {
                        clearInterval(timerInterval);
                        timerContainer.innerHTML = "<div class='text-center w-100'><h4 class='text-warning' style='font-family: \"Playfair Display\", serif;'>CHƯƠNG TRÌNH ĐÃ KẾT THÚC</h4></div>";
                        return;
                    }
                    
                    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
                    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                    const seconds = Math.floor((distance % (1000 * 60)) / 1000);
                    
                    timerContainer.innerHTML = \
                        <div class="text-center luxury-timer-box">
                            <div class="display-5 fw-bold" style="color: #ffffff; text-shadow: 0 0 10px rgba(255,255,255,0.3); font-family: 'Playfair Display', serif;">\</div>
                            <div class="small text-uppercase mt-2" style="color: #d4af37; letter-spacing: 2px; font-weight: 600; font-size: 0.7rem;">Ngày</div>
                        </div>
                        <div class="text-center luxury-timer-box">
                            <div class="display-5 fw-bold" style="color: #ffffff; text-shadow: 0 0 10px rgba(255,255,255,0.3); font-family: 'Playfair Display', serif;">\</div>
                            <div class="small text-uppercase mt-2" style="color: #d4af37; letter-spacing: 2px; font-weight: 600; font-size: 0.7rem;">Giờ</div>
                        </div>
                        <div class="text-center luxury-timer-box">
                            <div class="display-5 fw-bold" style="color: #ffffff; text-shadow: 0 0 10px rgba(255,255,255,0.3); font-family: 'Playfair Display', serif;">\</div>
                            <div class="small text-uppercase mt-2" style="color: #d4af37; letter-spacing: 2px; font-weight: 600; font-size: 0.7rem;">Phút</div>
                        </div>
                        <div class="text-center luxury-timer-box">
                            <div class="display-5 fw-bold" style="color: #ffffff; text-shadow: 0 0 10px rgba(255,255,255,0.3); font-family: 'Playfair Display', serif;">\</div>
                            <div class="small text-uppercase mt-2" style="color: #d4af37; letter-spacing: 2px; font-weight: 600; font-size: 0.7rem;">Giây</div>
                        </div>
                    \;
                }, 1000);
            }
        }
    });'''

    js_new = '''    // Countdown Timer JS (Multiple)
    document.addEventListener("DOMContentLoaded", function() {
        const timerContainers = document.querySelectorAll('.sale-countdown-timer');
        timerContainers.forEach(function(timerContainer) {
            const endDateStr = timerContainer.getAttribute('data-endtime');
            if (endDateStr) {
                const endDate = new Date(endDateStr).getTime();
                
                const timerInterval = setInterval(function() {
                    const now = new Date().getTime();
                    const distance = endDate - now;
                    
                    if (distance < 0) {
                        clearInterval(timerInterval);
                        timerContainer.innerHTML = "<div class='text-center w-100'><h4 class='text-warning' style='font-family: \"Playfair Display\", serif;'>CHƯƠNG TRÌNH ĐÃ KẾT THÚC</h4></div>";
                        return;
                    }
                    
                    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
                    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                    const seconds = Math.floor((distance % (1000 * 60)) / 1000);
                    
                    timerContainer.innerHTML = \
                        <div class="text-center luxury-timer-box">
                            <div class="display-5 fw-bold" style="color: #ffffff; text-shadow: 0 0 10px rgba(255,255,255,0.3); font-family: 'Playfair Display', serif;">\</div>
                            <div class="small text-uppercase mt-2" style="color: #d4af37; letter-spacing: 2px; font-weight: 600; font-size: 0.7rem;">Ngày</div>
                        </div>
                        <div class="text-center luxury-timer-box">
                            <div class="display-5 fw-bold" style="color: #ffffff; text-shadow: 0 0 10px rgba(255,255,255,0.3); font-family: 'Playfair Display', serif;">\</div>
                            <div class="small text-uppercase mt-2" style="color: #d4af37; letter-spacing: 2px; font-weight: 600; font-size: 0.7rem;">Giờ</div>
                        </div>
                        <div class="text-center luxury-timer-box">
                            <div class="display-5 fw-bold" style="color: #ffffff; text-shadow: 0 0 10px rgba(255,255,255,0.3); font-family: 'Playfair Display', serif;">\</div>
                            <div class="small text-uppercase mt-2" style="color: #d4af37; letter-spacing: 2px; font-weight: 600; font-size: 0.7rem;">Phút</div>
                        </div>
                        <div class="text-center luxury-timer-box">
                            <div class="display-5 fw-bold" style="color: #ffffff; text-shadow: 0 0 10px rgba(255,255,255,0.3); font-family: 'Playfair Display', serif;">\</div>
                            <div class="small text-uppercase mt-2" style="color: #d4af37; letter-spacing: 2px; font-weight: 600; font-size: 0.7rem;">Giây</div>
                        </div>
                    \;
                }, 1000);
            }
        });
    });'''

    html = html.replace(js_old, js_new)

    with open('templates/home.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Replaced successfully')
else:
    print('Failed to find replace block')

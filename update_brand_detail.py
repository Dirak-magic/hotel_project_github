import re
with open('templates/brand_detail.html', 'r', encoding='utf-8') as f:
    html = f.read()

sale_block = '''            <!-- BANNER KHUYẾN MÃI CỦA CƠ SỞ -->
            {% if prop.sale_active %}
            <div class="row mb-5">
                <div class="col-12">
                    <div class="card bg-dark text-white border-0 rounded-4 overflow-hidden shadow-lg position-relative">
                        <img src="{% if prop.sale_background %}{{ prop.sale_background.url }}{% else %}https://images.unsplash.com/photo-1571896349842-33c89424de2d?q=80&w=2000&auto=format&fit=crop{% endif %}" class="card-img" style="height: 350px; object-fit: cover; opacity: 0.5;" alt="Sale Banner">
                        <div class="card-img-overlay d-flex flex-column justify-content-center p-md-5">
                            <div class="row align-items-center w-100">
                                <div class="col-md-7">
                                    <span class="badge bg-danger mb-3 px-3 py-2 text-uppercase fw-bold" style="letter-spacing: 2px;">Ưu đãi đặc quyền</span>
                                    <h2 class="card-title display-5 fw-bold mb-3" style="font-family: 'Playfair Display', serif; color: #fce38a;">{{ prop.sale_title }}</h2>
                                    <p class="card-text fs-5 mb-4" style="opacity: 0.9;">{{ prop.sale_description|linebreaksbr }}</p>
                                    {% if prop.sale_button_link %}
                                    <a href="{{ prop.sale_button_link }}" target="_blank" class="btn btn-warning px-5 py-3 text-dark fw-bold rounded-pill text-uppercase" style="letter-spacing: 1px;">{{ prop.sale_button_text }}</a>
                                    {% endif %}
                                </div>
                                <div class="col-md-5 mt-4 mt-md-0 d-flex justify-content-md-end">
                                    <div class="d-flex flex-wrap justify-content-start justify-content-md-end gap-2 countdown-wrapper sale-countdown-timer" data-endtime="{{ prop.sale_end_date|date:'c' }}">
                                        <!-- Javascript sẽ tự động điền đếm ngược vào đây -->
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            {% endif %}

'''

html = html.replace('<!-- Danh sách Hạng phòng (Di chuyển LÊN TRÊN) -->', sale_block + '<!-- Danh sách Hạng phòng (Di chuyển LÊN TRÊN) -->')

# We also need to add the countdown javascript at the bottom of the file
js_code = '''
<script>
    // Countdown Timer JS cho các cơ sở
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
                        timerContainer.innerHTML = "<div class='text-center w-100'><h4 class='text-warning' style='font-family: \\"Playfair Display\\", serif;'>CHƯƠNG TRÌNH ĐÃ KẾT THÚC</h4></div>";
                        return;
                    }
                    
                    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
                    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                    const seconds = Math.floor((distance % (1000 * 60)) / 1000);
                    
                    timerContainer.innerHTML = \
                        <div class="text-center p-2 mx-1 rounded" style="background: rgba(0,0,0,0.5); border: 1px solid rgba(212, 175, 55, 0.5); min-width: 60px;">
                            <div class="fs-4 fw-bold text-white">\</div>
                            <div class="small" style="color: #d4af37; font-size: 0.7rem;">NGÀY</div>
                        </div>
                        <div class="text-center p-2 mx-1 rounded" style="background: rgba(0,0,0,0.5); border: 1px solid rgba(212, 175, 55, 0.5); min-width: 60px;">
                            <div class="fs-4 fw-bold text-white">\</div>
                            <div class="small" style="color: #d4af37; font-size: 0.7rem;">GIỜ</div>
                        </div>
                        <div class="text-center p-2 mx-1 rounded" style="background: rgba(0,0,0,0.5); border: 1px solid rgba(212, 175, 55, 0.5); min-width: 60px;">
                            <div class="fs-4 fw-bold text-white">\</div>
                            <div class="small" style="color: #d4af37; font-size: 0.7rem;">PHÚT</div>
                        </div>
                        <div class="text-center p-2 mx-1 rounded" style="background: rgba(0,0,0,0.5); border: 1px solid rgba(212, 175, 55, 0.5); min-width: 60px;">
                            <div class="fs-4 fw-bold text-white">\</div>
                            <div class="small" style="color: #d4af37; font-size: 0.7rem;">GIÂY</div>
                        </div>
                    \;
                }, 1000);
            }
        });
    });
</script>
'''

html += js_code

with open('templates/brand_detail.html', 'w', encoding='utf-8') as f:
    f.write(html)

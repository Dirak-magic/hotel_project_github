import re

with open('templates/home.html', 'r', encoding='utf-8') as f:
    text = f.read()

js_old = '''<script>
    // Countdown Timer JS (Restored)
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
                        timerContainer.innerHTML = "<div class='text-center w-100'><h4 class='text-warning' style='font-family: \\"Playfair Display\\", serif;'>CHƯƠNG TRÌNH ĐÃ KẾT THÚC</h4></div>";
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
    });
</script>'''

js_new = '''<script>
    // Force start the carousel
    document.addEventListener("DOMContentLoaded", function() {
        var myCarousel = document.querySelector('#saleCarousel');
        if (myCarousel) {
            var carousel = new bootstrap.Carousel(myCarousel, {
                interval: 4000,
                ride: 'carousel'
            });
            carousel.cycle();
        }
    });

    // Countdown Timer JS (Multiple)
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
    });
</script>'''

if js_old in text:
    text = text.replace(js_old, js_new)
    with open('templates/home.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced JS successfully")
else:
    print("Could not find js_old to replace!")

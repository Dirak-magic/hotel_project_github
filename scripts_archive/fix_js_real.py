import re

with open('templates/home.html', 'r', encoding='utf-8') as f:
    text = f.read()

js_pattern = r'// Countdown Timer JS \(Multiple\).*?(?=</script>)'

js_new = '''// Countdown Timer JS (Multiple)
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
                    
                    timerContainer.innerHTML = `
                        <div class="text-center luxury-timer-box">
                            <div class="display-5 fw-bold" style="color: #ffffff; text-shadow: 0 0 10px rgba(255,255,255,0.3); font-family: 'Playfair Display', serif;">${days}</div>
                            <div class="small text-uppercase mt-2" style="color: #d4af37; letter-spacing: 2px; font-weight: 600; font-size: 0.7rem;">Ngày</div>
                        </div>
                        <div class="text-center luxury-timer-box">
                            <div class="display-5 fw-bold" style="color: #ffffff; text-shadow: 0 0 10px rgba(255,255,255,0.3); font-family: 'Playfair Display', serif;">${hours.toString().padStart(2, '0')}</div>
                            <div class="small text-uppercase mt-2" style="color: #d4af37; letter-spacing: 2px; font-weight: 600; font-size: 0.7rem;">Giờ</div>
                        </div>
                        <div class="text-center luxury-timer-box">
                            <div class="display-5 fw-bold" style="color: #ffffff; text-shadow: 0 0 10px rgba(255,255,255,0.3); font-family: 'Playfair Display', serif;">${minutes.toString().padStart(2, '0')}</div>
                            <div class="small text-uppercase mt-2" style="color: #d4af37; letter-spacing: 2px; font-weight: 600; font-size: 0.7rem;">Phút</div>
                        </div>
                        <div class="text-center luxury-timer-box">
                            <div class="display-5 fw-bold" style="color: #ffffff; text-shadow: 0 0 10px rgba(255,255,255,0.3); font-family: 'Playfair Display', serif;">${seconds.toString().padStart(2, '0')}</div>
                            <div class="small text-uppercase mt-2" style="color: #d4af37; letter-spacing: 2px; font-weight: 600; font-size: 0.7rem;">Giây</div>
                        </div>
                    `;
                }, 1000);
            }
        });
    });
'''
text = re.sub(js_pattern, js_new, text, flags=re.DOTALL)

with open('templates/home.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Fixed syntax error in JS')

import re

with open('templates/home.html', 'r', encoding='utf-8') as f:
    text = f.read()

amenities_block = '''    <!-- Dải Icon Tiện Ích Toàn Cầu (Đưa ra khỏi carousel-inner để giữ cố định bên dưới) -->
    <div class="container-fluid py-5 bg-transparent border-0 position-relative" style="border-top: 1px solid rgba(255,255,255,0.05) !important; margin-top: 0; z-index: 10;">
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
</div>'''

new_block = '''</div>
    <!-- Dải Icon Tiện Ích Toàn Cầu (Đưa ra khỏi carousel-inner để giữ cố định bên dưới) -->
    <div class="container-fluid py-5 bg-transparent border-0 position-relative" style="border-top: 1px solid rgba(255,255,255,0.05) !important; margin-top: 0; z-index: 10;">
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
    </div>'''

if amenities_block in text:
    text = text.replace(amenities_block, new_block)
    with open('templates/home.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Moved amenities outside of saleCarousel successfully.")
else:
    print("Could not find amenities block exactly as formatted.")

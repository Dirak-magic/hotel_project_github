import re
with open('templates/brand_detail.html', 'r', encoding='utf-8') as f:
    text = f.read()

# First, remove the sale_block from inside the for loop
# The block starts with "            <!-- BANNER KHUYẾN MÃI CỦA CƠ SỞ -->" and ends with "            {% endif %}\n\n            <!-- Danh sách Hạng phòng"

# Let's use regex to remove it
text = re.sub(r'\s*<!-- BANNER KHUYẾN MÃI CỦA CƠ SỞ -->.*?{% endif %}', '', text, flags=re.DOTALL)

# Now, add it to the top, before the tabs.
# Look for "<div class=\"container py-5\">\n    <!-- Nav Tabs cho Các Cơ sở -->"
# Wait, "Các Cơ sở" should be renamed to "Các Chi nhánh" in the HTML comment, but let's just find "Nav Tabs"

insert_point = text.find('<div class="container py-5">\n    <!-- Nav Tabs')
if insert_point == -1:
    # try another match
    insert_point = text.find('    <!-- Nav Tabs cho Các Cơ sở -->')

if insert_point != -1:
    new_sale_block = '''    <!-- BANNER KHUYẾN MÃI CỦA CƠ SỞ -->
    {% if brand.sale_active %}
    <div class="row mb-5">
        <div class="col-12">
            <div class="card bg-dark text-white border-0 rounded-4 overflow-hidden shadow-lg position-relative">
                <img src="{% if brand.sale_background %}{{ brand.sale_background.url }}{% else %}https://images.unsplash.com/photo-1571896349842-33c89424de2d?q=80&w=2000&auto=format&fit=crop{% endif %}" class="card-img" style="height: 350px; object-fit: cover; opacity: 0.5;" alt="Sale Banner">
                <div class="card-img-overlay d-flex flex-column justify-content-center p-md-5">
                    <div class="row align-items-center w-100">
                        <div class="col-md-7">
                            <span class="badge bg-danger mb-3 px-3 py-2 text-uppercase fw-bold" style="letter-spacing: 2px;">Ưu đãi đặc quyền</span>
                            <h2 class="card-title display-5 fw-bold mb-3" style="font-family: 'Playfair Display', serif; color: #fce38a;">{{ brand.sale_title }}</h2>
                            <p class="card-text fs-5 mb-4" style="opacity: 0.9;">{{ brand.sale_description|linebreaksbr }}</p>
                            {% if brand.sale_button_link %}
                            <a href="{{ brand.sale_button_link }}" target="_blank" class="btn btn-warning px-5 py-3 text-dark fw-bold rounded-pill text-uppercase" style="letter-spacing: 1px;">{{ brand.sale_button_text }}</a>
                            {% endif %}
                        </div>
                        <div class="col-md-5 mt-4 mt-md-0 d-flex justify-content-md-end">
                            <div class="d-flex flex-wrap justify-content-start justify-content-md-end gap-2 countdown-wrapper sale-countdown-timer" data-endtime="{{ brand.sale_end_date|date:'c' }}">
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
    # We will insert it inside <div class="container py-5">, before the Nav Tabs
    text = text[:insert_point] + new_sale_block + text[insert_point:]
    
    with open('templates/brand_detail.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed brand_detail.html")
else:
    print("Could not find insert point in brand_detail.html")


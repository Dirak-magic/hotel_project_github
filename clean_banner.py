import re

with open('templates/brand_detail.html', 'r', encoding='utf-8') as f:
    text = f.read()

# First, remove the corrupted leftover part
corrupted_leftover = '''" class="card-img" style="height: 350px; object-fit: cover; opacity: 0.5;" alt="Sale Banner">
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
    {% endif %}'''

if corrupted_leftover in text:
    text = text.replace(corrupted_leftover, '')
else:
    # use regex
    text = re.sub(r'\" class=\"card-img\".*?{% endif %}', '', text, flags=re.DOTALL)

with open('templates/brand_detail.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Cleaned up corrupted banner')

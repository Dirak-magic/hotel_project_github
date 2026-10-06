import re
with open('templates/brand_detail.html', 'r', encoding='utf-8') as f:
    text = f.read()

leftover = '''                                </div>
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
            {% endif %}'''

if leftover in text:
    text = text.replace(leftover, '')
    with open('templates/brand_detail.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed leftover block!')
else:
    print('Leftover block not found. Trying regex.')
    text = re.sub(r'\s*</div>\s*<div class="col-md-5 mt-4 mt-md-0 d-flex justify-content-md-end">.*?{% endif %}\s*(?=<!-- Danh sách Hạng phòng)', '\n\n            ', text, flags=re.DOTALL)
    with open('templates/brand_detail.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed with regex')

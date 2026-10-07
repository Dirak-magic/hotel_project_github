import re
with open('core/models.py', 'r', encoding='utf-8') as f:
    text = f.read()

sale_fields = '''    # Các trường dành cho Chiến dịch Khuyến mãi (Flash Sale)
    sale_active = models.BooleanField(default=False, verbose_name="Bật chương trình Khuyến mãi")
    sale_title = models.CharField(max_length=100, blank=True, verbose_name="Tiêu đề Khuyến mãi", default="CHƯƠNG TRÌNH MÙA LƯỜI")
    sale_description = models.TextField(blank=True, verbose_name="Mô tả & Tiện ích tặng kèm")
    sale_end_date = models.DateTimeField(blank=True, null=True, verbose_name="Thời gian kết thúc (Đếm ngược)")
    sale_background = models.ImageField(upload_to="backgrounds/", blank=True, null=True, verbose_name="Ảnh nền Banner Sale")
    sale_button_text = models.CharField(max_length=50, blank=True, verbose_name="Chữ trên nút", default="XEM BẢNG GIÁ NGAY")
    sale_button_link = models.CharField(max_length=255, blank=True, verbose_name="Link nút bấm (URL)")

'''
text = re.sub(r'(    class Meta:\n        verbose_name = "Cơ sở \(Brand\)")', sale_fields + r'\1', text)

with open('core/models.py', 'w', encoding='utf-8') as f:
    f.write(text)

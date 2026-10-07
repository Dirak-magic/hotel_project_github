import re
with open('core/models.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Rename Brand verbose_name
text = text.replace(
'''    class Meta:
        verbose_name = "Thương hiệu"
        verbose_name_plural = "1. Các Thương hiệu"''',
'''    class Meta:
        verbose_name = "Cơ sở (Brand)"
        verbose_name_plural = "1. Các Cơ sở (Tuy Hòa, Chamhouse...)"'''
)

# 2. Add sale fields to Brand (right before class Meta)
sale_fields = '''    # Các trường dành cho Chiến dịch Khuyến mãi (Flash Sale)
    sale_active = models.BooleanField(default=False, verbose_name="Bật chương trình Khuyến mãi")
    sale_title = models.CharField(max_length=100, blank=True, verbose_name="Tiêu đề Khuyến mãi", default="CHƯƠNG TRÌNH MÙA LƯỜI")
    sale_description = models.TextField(blank=True, verbose_name="Mô tả & Tiện ích tặng kèm")
    sale_end_date = models.DateTimeField(blank=True, null=True, verbose_name="Thời gian kết thúc (Đếm ngược)")
    sale_background = models.ImageField(upload_to="backgrounds/", blank=True, null=True, verbose_name="Ảnh nền Banner Sale")
    sale_button_text = models.CharField(max_length=50, blank=True, verbose_name="Chữ trên nút", default="XEM BẢNG GIÁ NGAY")
    sale_button_link = models.CharField(max_length=255, blank=True, verbose_name="Link nút bấm (URL)")

'''
text = text.replace('    class Meta:\n        verbose_name = "Cơ sở (Brand)"', sale_fields + '    class Meta:\n        verbose_name = "Cơ sở (Brand)"')

# 3. Rename Property verbose_name
text = text.replace(
'''    class Meta:
        verbose_name = "Cơ sở (Chi nhánh)"
        verbose_name_plural = "2. Các Cơ sở (Chi nhánh)"''',
'''    class Meta:
        verbose_name = "Chi nhánh (Property)"
        verbose_name_plural = "2. Các Chi nhánh (Trường Chinh...)"'''
)

# 4. Remove sale fields from Property
text = re.sub(r'    # Các trường dành cho Chiến dịch Khuyến mãi.*?sale_button_link = models\.CharField[^\n]*\n', '', text, flags=re.DOTALL)

with open('core/models.py', 'w', encoding='utf-8') as f:
    f.write(text)

import re
with open('core/admin.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove from PropertyAdmin
text = text.replace('''        ('Chương trình Khuyến mãi (Flash Sale)', {
            'fields': ('sale_active', 'sale_title', 'sale_description', 'sale_end_date', 'sale_background', 'sale_button_text', 'sale_button_link'),
            'classes': ('collapse',),
            'description': 'Cấu hình chương trình Khuyến mãi riêng cho cơ sở này.'
        }),
''', '')

# Add to BrandAdmin
text = text.replace(
'''    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)''',
'''    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'slug', 'logo', 'banner', 'primary_color', 'description')
        }),
        ('Chương trình Khuyến mãi (Flash Sale)', {
            'fields': ('sale_active', 'sale_title', 'sale_description', 'sale_end_date', 'sale_background', 'sale_button_text', 'sale_button_link'),
            'classes': ('collapse',),
            'description': 'Cấu hình chương trình Khuyến mãi riêng cho cơ sở này.'
        }),
    )'''
)

with open('core/admin.py', 'w', encoding='utf-8') as f:
    f.write(text)

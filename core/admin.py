from django.contrib import admin
from django import forms
from .models import Brand, Property, RoomCategory, SiteSetting, RoomImage, FAQ, Amenity

# Thay đổi Tiêu đề trang Admin
admin.site.site_header = 'HỆ THỐNG QUẢN TRỊ KHÁCH SẠN'
admin.site.site_title = 'Trang quản trị'
admin.site.index_title = 'Bảng điều khiển (Dashboard)'

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class FAQInline(admin.StackedInline):
    model = FAQ
    extra = 1
    classes = ['collapse']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    inlines = [FAQInline]
    list_display = ('name', 'slug', 'primary_color')
    prepopulated_fields = {'slug': ('name',)}
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
    )

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'hotline', 'email')
    list_filter = ('brand',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'address')
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('brand', 'name', 'slug', 'address', 'hotline', 'email', 'facebook_link')
        }),
        ('Giao diện & Bản đồ', {
            'fields': ('background_image', 'google_maps_iframe')
        }),
        ('Tích hợp Google Sheets', {
            'fields': ('google_sheet_credentials', 'google_sheet_id'),
            'classes': ('collapse',)
        }),
    )

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={'multiple': True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class RoomCategoryAdminForm(forms.ModelForm):
    gallery_images = MultipleFileField(
        widget=MultipleFileInput(attrs={'multiple': True}),
        required=False,
        label="TẢI LÊN HÀNG LOẠT ẢNH (GALLERY)",
        help_text="Bấm Browse... sau đó bôi đen (hoặc giữ phím Ctrl) để chọn nhiều ảnh cùng lúc từ máy tính của bạn."
    )
    class Meta:
        model = RoomCategory
        fields = '__all__'

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 0
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            from django.utils.html import format_html
            return format_html('<img src="{}" style="height: 50px; border-radius: 5px;" />', obj.image.url)
        return ""
    image_preview.short_description = 'Xem trước'

@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    form = RoomCategoryAdminForm
    list_display = ('name', 'property', 'base_price', 'sale_price', 'weekend_surcharge')
    list_editable = ('base_price', 'sale_price', 'weekend_surcharge')
    list_filter = ('property__brand', 'property')
    search_fields = ('name',)
    inlines = [RoomImageInline]
    filter_horizontal = ('amenities',)
    fieldsets = (
        ('Thông tin phòng', {
            'fields': ('property', 'name', 'cover_image', 'description', 'amenities')
        }),
        ('Giá & Phụ thu', {
            'fields': ('base_price', 'sale_price', 'weekend_surcharge')
        }),
        ('Chính sách & Giờ giấc', {
            'fields': ('checkin_time', 'checkout_time', 'custom_policies')
        }),
        ('Đồng bộ Google Sheets', {
            'fields': ('sheet_row_name',),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        for f in request.FILES.getlist('gallery_images'):
            RoomImage.objects.create(room=obj, image=f)

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name',)
    fieldsets = (
        ('Cấu hình chung', {
            'fields': ('site_name', 'footer_text', 'hotline', 'facebook_link', 'homepage_background', 'homepage_background_video')
        }),
        ('Khu vực Video Giới thiệu', {
            'fields': ('promo_video_url', 'promo_video_bg'),
            'description': 'Cấu hình khu vực Video Pop-up (Nút Play Vàng) trên trang chủ.'
        }),
    )
    def has_add_permission(self, request):
        if SiteSetting.objects.exists():
            return False
        return True

# Tùy chỉnh lại giao diện OTP TOTP Device để dễ dùng hơn (biến ô nhập User thành Dropdown)
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin

try:
    admin.site.unregister(TOTPDevice)
except Exception:
    pass

class CustomTOTPDeviceAdmin(TOTPDeviceAdmin):
    raw_id_fields = ()  # Tắt cái kính lúp đi để biến thành Dropdown chọn tài khoản

admin.site.register(TOTPDevice, CustomTOTPDeviceAdmin)

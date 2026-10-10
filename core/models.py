from django.utils import timezone
from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên thương hiệu")
    slug = models.SlugField(unique=True, help_text="VD: ambergris, handstay")
    logo = models.ImageField(upload_to='brands/logos/', verbose_name="Logo")
    banner = models.ImageField(upload_to='brands/banners/', blank=True, null=True, verbose_name='Ảnh Banner (Trang chi tiết)')
    primary_color = models.CharField(max_length=7, default='#000000', help_text="Mã màu HEX (VD: Chamhouse là #9e4333)", verbose_name="Màu chủ đạo")
    description = models.TextField(blank=True, verbose_name="Giới thiệu chung")


    # Các trường dành cho Chiến dịch Khuyến mãi (Flash Sale)
    sale_active = models.BooleanField(default=False, verbose_name="Bật chương trình Khuyến mãi")
    sale_title = models.CharField(max_length=100, blank=True, verbose_name="Tiêu đề Khuyến mãi", default="CHƯƠNG TRÌNH MÙA LƯỜI")
    sale_description = models.TextField(blank=True, verbose_name="Mô tả & Tiện ích tặng kèm")
    sale_end_date = models.DateTimeField(blank=True, null=True, verbose_name="Thời gian kết thúc (Đếm ngược)")
    sale_background = models.ImageField(upload_to="backgrounds/", blank=True, null=True, verbose_name="Ảnh nền Banner Sale")
    sale_button_text = models.CharField(max_length=50, blank=True, verbose_name="Chữ trên nút", default="XEM BẢNG GIÁ NGAY")
    sale_button_link = models.CharField(max_length=255, blank=True, verbose_name="Link nút bấm (URL)")

    class Meta:
        verbose_name = "Cơ sở (Brand)"
        verbose_name_plural = "1. Các Cơ sở (Tuy Hòa, Chamhouse...)"

    def __str__(self):
        return self.name

class Property(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='properties', verbose_name="Thương hiệu trực thuộc")
    name = models.CharField(max_length=100, verbose_name="Tên cơ sở")
    slug = models.SlugField(unique=True, verbose_name="Đường dẫn (Slug)")
    address = models.CharField(max_length=255, verbose_name="Địa chỉ cụ thể")
    google_maps_iframe = models.TextField(blank=True, verbose_name="Mã nhúng Bản đồ", help_text="Vào Google Maps > Chia sẻ > Nhúng bản đồ > Copy iframe")
    hotline = models.CharField(max_length=20, blank=True, verbose_name="Hotline")
    email = models.EmailField(blank=True, verbose_name="Email liên hệ")
    facebook_link = models.URLField(blank=True, verbose_name="Link Facebook")
    background_image = models.ImageField(upload_to="properties/backgrounds/", blank=True, null=True, verbose_name="Ảnh nền Website (Full toàn trang)")
    
    from django.core.files.storage import FileSystemStorage
    from django.conf import settings
    private_storage = FileSystemStorage(location=settings.MEDIA_ROOT)
    
    google_sheet_credentials = models.FileField(storage=private_storage, upload_to='credentials/', blank=True, null=True, verbose_name='File JSON Credentials (Google API)')
    google_sheet_id = models.CharField(max_length=150, blank=True, verbose_name="Google Sheet ID", help_text="Chuỗi ký tự nằm giữa /d/ và /edit trong link Google Sheet")


    class Meta:
        verbose_name = "Chi nhánh (Property)"
        verbose_name_plural = "2. Các Chi nhánh (Trường Chinh...)"

    def __str__(self):
        return f"{self.brand.name} - {self.name}"

class Amenity(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên tiện ích (VD: Wi-Fi Miễn phí)")

    class Meta:
        verbose_name = 'Tiện ích'
        verbose_name_plural = '3. Các Tiện ích'

    def __str__(self):
        return self.name

class RoomCategory(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='room_categories', verbose_name="Cơ sở")
    name = models.CharField(max_length=100, verbose_name="Tên hạng phòng")
    amenities = models.ManyToManyField(Amenity, blank=True, related_name="rooms", verbose_name="Các tiện ích có trong phòng")
    base_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Giá tham khảo")
    sale_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, verbose_name="Giá khuyến mãi")
    weekend_surcharge = models.IntegerField(default=0, verbose_name="Phụ thu cuối tuần (VNĐ)", help_text="Số tiền cộng thêm vào Thứ 6, Thứ 7, Chủ Nhật")
    description = models.TextField(verbose_name="Mô tả phòng")
    cover_image = models.ImageField(upload_to='rooms/covers/', verbose_name="Ảnh bìa")
    
    sheet_row_name = models.CharField(max_length=150, blank=True, verbose_name="Tên phòng trên Google Sheet", help_text="1 phòng: 'ROOM A' | Nhiều phòng (Handstay): 'R1, R2, R3' | Phòng gộp: 'R4 + R5'")
    
    checkin_time = models.CharField(max_length=50, default="14:00", verbose_name="Giờ Nhận phòng (Check-in)")
    checkout_time = models.CharField(max_length=50, default="12:00", verbose_name="Giờ Trả phòng (Check-out)")
    custom_policies = models.TextField(blank=True, verbose_name="Chính sách & Lưu ý riêng (Tùy chọn)")

    class Meta:
        verbose_name = "Hạng phòng"
        verbose_name_plural = "4. Các Hạng phòng"

    def is_weekend_now(self):
        # 4=Thứ 6, 5=Thứ 7, 6=Chủ Nhật
        return timezone.now().weekday() in [4, 5, 6]
        
    def display_original_price(self):
        # Yêu cầu: Giá gốc sẽ không cộng phụ thu cuối tuần
        return self.base_price
        
    def display_price(self):
        current = self.sale_price if self.sale_price else self.base_price
        if self.is_weekend_now():
            return current + self.weekend_surcharge
        return current

    def __str__(self):
        return f"[{self.property.name}] {self.name}"

class RoomImage(models.Model):
    room = models.ForeignKey(RoomCategory, related_name='images', on_delete=models.CASCADE, verbose_name="Hạng phòng")
    image = models.ImageField(upload_to='rooms/gallery/', verbose_name="Ảnh chi tiết")
    
    class Meta:
        verbose_name = "Ảnh chi tiết phòng"
        verbose_name_plural = "Ảnh chi tiết phòng"

    def __str__(self):
        return f"Ảnh của {self.room.name}"

class SiteSetting(models.Model):
    homepage_background = models.ImageField(upload_to="backgrounds/", blank=True, null=True, verbose_name="Ảnh nền Trang chủ")
    homepage_background_video = models.FileField(upload_to="backgrounds/videos/", blank=True, null=True, verbose_name="Video nền Trang chủ (MP4)", help_text="Sẽ ưu tiên dùng Video thay cho Ảnh nền nếu có")
    site_name = models.CharField(max_length=50, default='AMBERGRIS', verbose_name='Tên Header')
    footer_text = models.CharField(max_length=255, default='© 2026 Ambergris.', verbose_name='Chữ Footer')
    facebook_link = models.URLField(blank=True, verbose_name='Link Facebook')
    hotline = models.CharField(max_length=20, blank=True, verbose_name='Hotline chung')
    promo_video_url = models.URLField(blank=True, verbose_name='Link Video Giới thiệu (Youtube)')
    promo_video_bg = models.ImageField(upload_to='backgrounds/', blank=True, null=True, verbose_name='Ảnh nền khu vực Video')
    disable_availability_check = models.BooleanField(default=False, verbose_name='Bảo trì tính năng Tra cứu lịch trống', help_text='Đánh dấu mục này để khóa người dùng tra cứu khi Google bị lỗi.')

    class Meta:
        verbose_name = 'Cấu hình Website'
        verbose_name_plural = '5. Cấu hình Website'

    def __str__(self):
        return 'Cấu hình chung'

class FAQ(models.Model):
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, related_name='faqs', null=True, blank=True, verbose_name="Thương hiệu")
    question = models.CharField(max_length=255, verbose_name="Câu hỏi (VD: Có chỗ đậu xe không?)")
    answer = models.TextField(verbose_name="Câu trả lời")
    order = models.IntegerField(default=0, verbose_name="Thứ tự ưu tiên")

    class Meta:
        verbose_name = 'Câu hỏi thường gặp (FAQ)'
        verbose_name_plural = 'Câu hỏi thường gặp (FAQ)'
        ordering = ['order', 'id']
        
    def __str__(self):
        return self.question


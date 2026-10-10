import os
import cloudinary.uploader
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Tải toàn bộ file trong thư mục media cục bộ lên Cloudinary'

    def handle(self, *args, **kwargs):
        media_root = settings.MEDIA_ROOT
        
        if not os.path.exists(media_root):
            self.stdout.write(self.style.ERROR('Media root not found.'))
            return
            
        self.stdout.write(f'Scanning directory: {media_root}')
        
        for root, dirs, files in os.walk(media_root):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Bỏ qua các file ẩn (như .DS_Store)
                if file.startswith('.'):
                    continue
                    
                # Tạo public_id cho Cloudinary (đường dẫn tương đối tính từ MEDIA_ROOT)
                # Ví dụ: file ở 'media/room_images/1.jpg' sẽ có public_id là 'room_images/1'
                relative_path = os.path.relpath(file_path, media_root)
                public_id, ext = os.path.splitext(relative_path)
                
                # django-cloudinary-storage mặc định thêm MEDIA_URL (thường là 'media/') vào public_id
                media_prefix = getattr(settings, 'MEDIA_URL', '/media/').strip('/')
                if media_prefix:
                    public_id = f"{media_prefix}/{public_id}".replace('\\', '/')
                else:
                    public_id = public_id.replace('\\', '/')
                
                try:
                    self.stdout.write(f'Uploading: {relative_path} ...', ending='')
                    
                    # Upload file lên Cloudinary
                    cloudinary.uploader.upload(
                        file_path,
                        public_id=public_id,
                        overwrite=True,
                        resource_type="auto" # tự động nhận diện ảnh/video/tệp
                    )
                    self.stdout.write(self.style.SUCCESS(' SUCCESS'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f' ERROR: {e}'))
                    
        self.stdout.write(self.style.SUCCESS('\nUpload complete!'))

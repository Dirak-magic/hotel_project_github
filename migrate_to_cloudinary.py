import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.files import File
from core.models import Brand, Property, RoomCategory, RoomImage, SiteSetting
from django.conf import settings

def migrate_field(instance, field_name):
    field_file = getattr(instance, field_name)
    if not field_file or not field_file.name:
        return
    
    local_path = os.path.join(settings.BASE_DIR, 'media', field_file.name)
    
    if os.path.exists(local_path):
        print(f"Uploading {field_file.name}...")
        try:
            with open(local_path, 'rb') as f:
                django_file = File(f)
                field_file.save(os.path.basename(field_file.name), django_file, save=True)
                print(f"-> Success! New URL: {field_file.url}")
                
            os.rename(local_path, local_path + ".uploaded")
        except Exception as e:
            print(f"Error uploading {field_file.name}: {e}")
    else:
        pass

def run():
    print("STARTING MIGRATION TO CLOUDINARY...")
    models_to_migrate = [
        (Brand, ['logo', 'banner', 'sale_background']),
        (Property, ['background_image']),
        (RoomCategory, ['cover_image']),
        (RoomImage, ['image']),
        (SiteSetting, ['homepage_background', 'homepage_background_video', 'promo_video_bg']),
    ]
    
    for model, fields in models_to_migrate:
        for obj in model.objects.all():
            for field in fields:
                migrate_field(obj, field)
                
    print("MIGRATION COMPLETE!")

if __name__ == '__main__':
    run()

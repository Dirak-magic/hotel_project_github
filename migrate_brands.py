import os
import re
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.files import File
from core.models import Brand, Property, SiteSetting
from django.conf import settings

def find_original_file(hashed_name):
    base_name = os.path.basename(hashed_name)
    match = re.match(r'(.*)_[a-zA-Z0-9]{7}(\.[^.]+)$', base_name)
    if match:
        original_name = match.group(1) + match.group(2)
        local_path = os.path.join(settings.BASE_DIR, 'media', os.path.dirname(hashed_name), original_name)
        if os.path.exists(local_path):
            return local_path
    
    local_path = os.path.join(settings.BASE_DIR, 'media', hashed_name)
    if os.path.exists(local_path):
        return local_path
        
    return None

def run():
    print("STARTING BRANDS/PROPERTIES MIGRATION TO CLOUDINARY...")
    for model, fields in [(Brand, ['logo', 'banner', 'sale_background']), 
                          (Property, ['background_image']),
                          (SiteSetting, ['homepage_background', 'promo_video_bg'])]:
        for obj in model.objects.all():
            for field in fields:
                field_file = getattr(obj, field)
                if not field_file or not field_file.name: 
                    continue
                
                local_path = find_original_file(field_file.name)
                if local_path:
                    try:
                        print(f"Uploading {field_file.name} from {local_path}...")
                        with open(local_path, 'rb') as f:
                            django_file = File(f)
                            field_file.save(os.path.basename(field_file.name), django_file, save=True)
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    print(f"Missing local file for {field_file.name}")
    print("MIGRATION COMPLETE!")

if __name__ == '__main__':
    run()

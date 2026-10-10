import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
import cloudinary.api
import cloudinary.uploader

def rename_all():
    next_cursor = None
    while True:
        res = cloudinary.api.resources(max_results=100, next_cursor=next_cursor)
        for img in res['resources']:
            old_id = img['public_id']
            if not old_id.startswith('media/'):
                new_id = f"media/{old_id}"
                print(f"Renaming {old_id} -> {new_id}")
                cloudinary.uploader.rename(old_id, new_id, overwrite=True)
        next_cursor = res.get('next_cursor')
        if not next_cursor:
            break
    print("Done renaming!")
rename_all()

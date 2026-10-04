import re

with open('core/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_view = """
def contact_view(request):
    from .models import Property, Brand
    properties = Property.objects.select_related('brand').all()
    all_brands = Brand.objects.all()
    return render(request, 'contact.html', {'properties': properties, 'all_brands': all_brands})
"""
if "def contact_view" not in text:
    text += new_view

with open('core/views.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Added contact_view to views.py")

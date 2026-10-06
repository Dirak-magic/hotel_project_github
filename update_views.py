import re
with open('core/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
'''def home(request):
    brands = Brand.objects.all()
    from .models import Property
    sale_properties = Property.objects.filter(sale_active=True)
    return render(request, 'home.html', {'brands': brands, 'sale_properties': sale_properties})''',
'''def home(request):
    brands = Brand.objects.all()
    sale_properties = Brand.objects.filter(sale_active=True)
    return render(request, 'home.html', {'brands': brands, 'sale_properties': sale_properties})'''
)

with open('core/views.py', 'w', encoding='utf-8') as f:
    f.write(text)

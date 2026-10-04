from modeltranslation.translator import register, TranslationOptions
from .models import Brand, Property, RoomCategory, SiteSetting, Amenity

@register(Brand)
class BrandTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Property)
class PropertyTranslationOptions(TranslationOptions):
    fields = ('name', 'address')

@register(Amenity)
class AmenityTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(RoomCategory)
class RoomCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(SiteSetting)
class SiteSettingTranslationOptions(TranslationOptions):
    fields = ('site_name', 'footer_text')

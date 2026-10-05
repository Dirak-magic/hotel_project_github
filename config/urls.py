from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django_otp.admin import OTPAdminSite
import django_otp

class FixOTPAdminSite(OTPAdminSite):
    def login(self, request, extra_context=None):
        response = super().login(request, extra_context)
        if request.user.is_authenticated and request.method == 'POST' and 'otp_token' in request.POST:
            # TOTP tokens are single-use. We cannot validate the form again (it will fail).
            # But since super().login() succeeded, we just fetch the device from POST and log it in.
            device_id = request.POST.get('otp_device')
            if device_id:
                from django_otp.models import Device
                device = Device.from_persistent_id(device_id)
                if device and device.user_id == request.user.id:
                    django_otp.login(request, device)
            else:
                # Fallback if device ID not in POST
                device = request.user.totpdevice_set.filter(confirmed=True).first()
                if device:
                    django_otp.login(request, device)
        return response

# Enforce 2FA for the admin site
admin.site.__class__ = FixOTPAdminSite

urlpatterns = [
    path('handamb-quanly/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

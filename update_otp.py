import re

with open('config/settings.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("'axes',", "'axes',\n    'django_otp',\n    'django_otp.plugins.otp_totp',")
text = text.replace("'django.contrib.auth.middleware.AuthenticationMiddleware',", "'django.contrib.auth.middleware.AuthenticationMiddleware',\n    'django_otp.middleware.OTPMiddleware',")

with open('config/settings.py', 'w', encoding='utf-8') as f:
    f.write(text)

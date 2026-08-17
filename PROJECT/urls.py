from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

# http://127.0.0.1:8000/  ==>  https://thedevu101.uz/
urlpatterns = [
    path('admin/', admin.site.urls),  # http://127.0.0.1:8000/admin/
    path('', include('app_main.urls')),

    path('password-reset/', PasswordResetView.as_view(template_name='password/password-reset.html'), name="password_reset"),
    path('password-reset-done/', PasswordResetDoneView.as_view(template_name='password/password-reset-done.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password/passport-reset-confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

urlpatterns += static(prefix=settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

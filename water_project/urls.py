from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from water_app.views import generate_pdf_report




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('water_app.urls')),
    path('generate_report/', generate_pdf_report, name='generate_pdf_report'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

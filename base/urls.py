from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('forside.urls')),
    path('arkiveringsversioner/', include('arkiveringsversioner.urls')),
    path('hardware/', include('hardware.urls')),
    path('statistik/', include('statistik.urls')),
    path('system/', include('system.urls')),
]

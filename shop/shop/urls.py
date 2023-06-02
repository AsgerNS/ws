from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('10/ws-shop/', include('ws.urls')),
]

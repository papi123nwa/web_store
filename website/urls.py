from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('gamestore.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^', include('allauth.urls')),
]

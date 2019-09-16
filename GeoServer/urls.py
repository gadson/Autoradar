"""GeoServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/v1/', include('api.url')),
    url(r'^view/', include('api.url')),
    url(r'^object/', include('api.url')),
    url(r'^backup/', include('api.url')),
    url(r'^password/', include('api.url')),
    url(r'^object_mobile/', include('api.url')),
    url(r'^edit/', include('api.url')),
    url(r'^edit_mobile/', include('api.url')),
    url(r'^add/', include('api.url')),
    url(r'^logout/', include('api.url')),
    url(r'^register/', include('api.url')),
    url(r'^login/', include('api.url')),
    url(r'^policy/', include('api.url')),
    url(r'^login_mobile/', include('api.url')),
    url(r'^register_mobile/', include('api.url')),
    url(r'^mobile/', include('api.url')),
    url(r'^', include('api.url')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
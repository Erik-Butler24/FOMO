"""FOMO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from catalog.views import views

router = routers.DefaultRouter()
router.register(r'', views.ProductViewSet)
router.register(r'categories', views.CategoryViewSet)

urlpatterns = [
    # the built-in Django administrator
    url(r'^admin/', admin.site.urls),

    url('catalog/search', include(router.urls)),

    # urls for any third-party apps go here

    # the DMP router - if DEFAULT_HOMEPAGE is set, this should be the last pattern (the wildcards match everything)
    url('', include('django_mako_plus.urls')),

    path('account/', include('django.contrib.auth.urls')),
]

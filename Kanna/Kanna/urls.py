"""Kanna URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import login_required
from django.contrib.auth.decorators import  user_passes_test
#
# login_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/lessons')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lessons/', include('lessons.urls')),
    path('', RedirectView.as_view(url='lessons/')),  # todo set homepage in own app
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # todo remove serving of static files on deploy


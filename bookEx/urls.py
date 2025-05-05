"""bookEx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin# Path: bookEx/urls.py
from django.urls import path# Path: bookEx/urls.py

from django.urls import include

from django.views.generic.base import TemplateView

from django.conf import settings
from django.conf.urls.static import static

from bookMng.views import Register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/success', TemplateView.as_view(
        template_name="registration/register_success.html"
    ), name='register-success'),
    path('register', Register.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
    path('', include('bookMng.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
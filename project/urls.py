"""project URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from app.views import TestView, index, login_user, logout_user, register_user

from rest_framework.authtoken.views import obtain_auth_token

# Dataframes app
from django.conf import settings
from django.conf.urls.static import static
# from django.urls import include


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api_test/', TestView.as_view(), name="api_test"),
    path('api/token/', obtain_auth_token, name='obtain-token'),
    path('rest-auth/', include('rest_auth.urls')),
    path('admin/', admin.site.urls),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
    path('register/', register_user, name="register"),
    path('', index, name="index"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)

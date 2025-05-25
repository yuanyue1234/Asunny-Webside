"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('lyb/', include('lyb.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from rest_framework import routers # 不再在这里定义 router
# from lyb.views import LybrViewSet, register_user, login_user # 这些将通过 lyb.urls 引入

# router = routers.DefaultRouter() # 移至 lyb.urls.py
# router.register(r'lyb', LybrViewSet) # 移至 lyb.urls.py

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/lyb/', include('lyb.urls')), # 包含 lyb app 的所有 URL
    # path('api/', include(router.urls)), # 旧的 lyb router，将被上面的取代
    # path('api/register/', register_user, name='register'), # 移至 lyb.urls.py
    # path('api/login/', login_user, name='login'), # 移至 lyb.urls.py
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LybrViewSet, NavItemListAPIView, register_user, login_user

# 创建一个路由器并注册我们的视图集。
router = DefaultRouter()
router.register(r'lyb', LybrViewSet, basename='lyb') # 为 LybrViewSet 定义 basename

urlpatterns = [
    path('', include(router.urls)), # 将路由器生成的URL包含进来
    path('navitems/', NavItemListAPIView.as_view(), name='navitem-list'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
] 
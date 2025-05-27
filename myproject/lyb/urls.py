from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LybrViewSet, NavItemListAPIView, register_user, login_user, get_user_info

# 创建一个路由器并注册我们的视图集。
router = DefaultRouter()
router.register(r'lyb', LybrViewSet)

urlpatterns = [
    path('', include(router.urls)), # 将路由器生成的URL包含进来
    path('navitems/', NavItemListAPIView.as_view(), name='nav-list'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('user/info/', get_user_info, name='user-info'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] 
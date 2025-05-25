from django.urls import path
from .views import SiteProfileAPIView

urlpatterns = [
    path('profile/', SiteProfileAPIView.as_view(), name='site-profile'),
] 
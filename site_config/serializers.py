from rest_framework import serializers
from .models import SiteProfile

class SiteProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteProfile
        fields = ['profile_data', 'last_updated']
        read_only_fields = ['last_updated'] # last_updated 由服务器自动更新 
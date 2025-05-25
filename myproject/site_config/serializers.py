from rest_framework import serializers
from .models import SiteProfile # 确保导入 SiteProfile

class SiteProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteProfile
        fields = ['profile_data', 'last_updated']
        read_only_fields = ['last_updated'] 
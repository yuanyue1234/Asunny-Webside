from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import SiteProfile
from .serializers import SiteProfileSerializer

class SiteProfileAPIView(APIView):
    """
    API endpoint for retrieving and updating the site profile.
    GET: Open to all for retrieving profile data.
    PUT: Restricted to admin users for updating profile data.
    """

    def get_object(self):
        # 使用模型的 get_solo 方法获取唯一的实例
        return SiteProfile.get_solo()

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = SiteProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        if not request.user.is_staff: # 或者更严格地使用 is_superuser
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        profile = self.get_object()
        # 我们只期望更新 profile_data 字段
        serializer = SiteProfileSerializer(profile, data=request.data, partial=True) # partial=True 允许部分更新
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
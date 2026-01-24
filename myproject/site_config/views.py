from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import SiteProfile
from .serializers import SiteProfileSerializer


class SiteProfileAPIView(APIView):
    """
    用于检索和更新站点配置文件的API端点。
    GET: 全部打开以检索配置文件数据。
    PUT: 仅限于管理员用户更新配置文件数据。
    """
    permission_classes = [permissions.AllowAny]  # 确保 GET 请求是公开的

    def get_object(self):
        # 使用模型的 get_solo 方法获取唯一的实例
        return SiteProfile.get_solo()

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = SiteProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        # 即使类级别是 AllowAny，PUT 请求仍然需要显式的权限检查
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )

        profile = self.get_object()
        serializer = SiteProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

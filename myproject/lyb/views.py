# 引入 Django 和 DRF（Django REST framework）相关模块
from django.shortcuts import render
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import lyb, NavItem
from .serializers import LybSerializer, NavItemSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

# 留言板视图集，提供增删改查接口
class LybrViewSet(viewsets.ModelViewSet):
    """
    提供留言板（lyb）模型的 API 接口，支持查看、创建、修改、删除留言。
    """
    queryset = lyb.objects.all().order_by('-posttime')  # 获取所有留言，按发布时间倒序排列
    serializer_class = LybSerializer  # 指定序列化器
    permission_classes = [permissions.AllowAny]  # 允许任何人访问（不需要登录）

# 用户注册接口
@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # 允许未登录用户访问
def register_user(request):
    """
    用户注册接口，接收用户名、密码和邮箱，创建新用户。
    """
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    # 检查用户名和密码是否为空
    if not username or not password:
        return Response({'error': '用户名和密码不能为空'}, status=status.HTTP_400_BAD_REQUEST)

    # 检查用户名是否已存在
    if User.objects.filter(username=username).exists():
        return Response({'error': '用户名已存在'}, status=status.HTTP_400_BAD_REQUEST)

    # 创建新用户
    user = User.objects.create_user(username=username, password=password, email=email)
    return Response({'message': '注册成功'}, status=status.HTTP_201_CREATED)

# 用户登录接口
@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # 允许未登录用户访问
def login_user(request):
    """
    用户登录接口，验证用户名和密码，返回 JWT Token。
    """
    username = request.data.get('username')
    password = request.data.get('password')

    # 检查用户名和密码是否为空
    if not username or not password:
        return Response({'error': '用户名和密码不能为空'}, status=status.HTTP_400_BAD_REQUEST)

    # 验证用户身份
    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'error': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)

    # 生成 JWT Token
    refresh = RefreshToken.for_user(user)
    return Response({
        'token': str(refresh.access_token),  # 访问令牌
        'refresh': str(refresh),            # 刷新令牌
        'username': user.username
    })

# 获取导航项列表的 API 视图
class NavItemListAPIView(APIView):
    permission_classes = [permissions.AllowAny]  # 允许任何人访问

    def get(self, request):
        """
        获取所有导航项（NavItem）并返回 JSON 数据。
        """
        nav_items = NavItem.objects.all()  # 获取所有导航项
        serializer = NavItemSerializer(nav_items, many=True)  # 序列化数据
        return Response(serializer.data)  # 返回响应

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    return Response({
        'username': user.username,
        'email': user.email,
        'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S')
    })

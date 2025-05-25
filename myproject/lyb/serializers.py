from rest_framework import serializers
from .models import lyb, NavItem


class LybSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = lyb
        # fields = ['title', 'author', 'content', 'posttime']
        fields = '__all__'

# 新增 NavItemSerializer
class NavItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavItem
        fields = ['id', 'text', 'url']

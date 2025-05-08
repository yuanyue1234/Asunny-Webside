from rest_framework import serializers
from .models import lyb


class LybSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = lyb
        # fields = ['title', 'author', 'content', 'posttime']
        fields = '__all__'

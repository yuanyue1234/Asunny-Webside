from django.shortcuts import render
from rest_framework import permissions, viewsets
from .models import lyb
from .serializers import LybSerializer


# Create your views here.
class LybrViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = lyb.objects.all().order_by('-posttime')
    serializer_class = LybSerializer

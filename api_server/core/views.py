from django.shortcuts import render
from rest_framework import viewsets
from .models import Trial
from .serializers import TrialSerializer


class TrialViewSet(viewsets.ModelViewSet):
    queryset = Trial.objects.all()
    serializer_class = TrialSerializer

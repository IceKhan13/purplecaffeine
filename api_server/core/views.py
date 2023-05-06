"""
Module to handle the views of API calls
"""
from rest_framework import viewsets
from .models import Trial
from .serializers import TrialSerializer


class TrialViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Trial model
    """

    queryset = Trial.objects.all()  # pylint: disable=no-member
    serializer_class = TrialSerializer

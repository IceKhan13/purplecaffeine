from rest_framework import viewsets
from .models import Trial
from .serializers import TrialSerializer


class TrialViewSet(viewsets.ModelViewSet):
    # ViewSet for Trial model.
    queryset = Trial.objects.all()
    serializer_class = TrialSerializer
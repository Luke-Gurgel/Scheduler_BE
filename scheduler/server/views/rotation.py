from rest_framework import viewsets
from ..serializers import RotationSerializer
from ..models import Rotation


class RotationViewSet(viewsets.ModelViewSet):
    queryset = Rotation.objects.all()
    serializer_class = RotationSerializer

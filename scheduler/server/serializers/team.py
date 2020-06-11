from rest_framework import serializers
from ..models import Team, TeamMember, Rotation


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = "__all__"


class RotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rotation
        fields = "__all__"

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from django.core.exceptions import ObjectDoesNotExist
from ..serializers import TeamSerializer, TeamMemberSerializer, RotationSerializer
from ..services import EmailService
from ..models import Team


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    lookup_field = "name"
    chief_only_response = Response(
        "This is a chief-only operation", status=status.HTTP_401_UNAUTHORIZED
    )

    def is_request_valid(self) -> bool:
        """Check if team member is chief."""
        team = self.get_object()
        try:
            team_member = team.teammember_set.get(pk=1)  # get id from JWT
            return team_member.is_chief
        except ObjectDoesNotExist:
            return False

    def partial_update(self, request, name=None):
        if self.is_request_valid():
            return self.partial_update(request, name)
        return self.chief_only_response

    def update(self, request, name=None):
        if self.is_request_valid():
            return self.update(request, name)
        return self.chief_only_response

    def destroy(self, request, name=None):
        if self.is_request_valid():
            return self.destroy(request, name)
        return self.chief_only_response

    @action(methods=["GET"], detail=True)
    def team_members(self, request, name=None):
        team = self.get_object()
        members = team.teammember_set.order_by("column_order_position")
        serializer = TeamMemberSerializer(members, many=True)
        return Response(serializer.data)

    @action(methods=["GET"], detail=True)
    def rotations(self, request, name=None):
        team = self.get_object()
        rotations = team.rotation_set.all()
        serializer = RotationSerializer(rotations, many=True)
        return Response(serializer.data)

    @action(methods=["POST"], detail=True)
    def invite(self, request: Request, name=None):
        try:
            email_client = EmailService()
            email_client.send_invite_email(
                team_name=name,
                to_emails=request.data["to_emails"],
                from_email=request.data["from_email"],
            )
            return Response("Invites sent successfully", status=status.HTTP_200_OK)
        except Exception:
            return Response(
                "We're sorry, the invites could not be sent",
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

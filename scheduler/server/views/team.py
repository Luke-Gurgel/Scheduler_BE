from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from ..serializers import TeamSerializer, TeamMemberSerializer
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
        team_member = team.teammember_set.get(pk=2)  # get id from JWT
        return team_member.is_chief

    def partial_update(self, request, name=None):
        if self.is_request_valid():
            return self.partial_update(request, name)
        return self.chief_only_response

    def udpate(self, request, name=None):
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


# list (admin) ✅
# get (all) ✅
# create (all) ✅
# update -> name (chiefs) ✅
# delete (chiefs) ✅
# GET / teams/<int:id>/team_members ✅
# POST /teams/invite/<int:id> -> invite members to a team

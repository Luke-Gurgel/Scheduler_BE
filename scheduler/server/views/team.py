from rest_framework.response import Response
from rest_framework import generics, status
from ..serializers import TeamSerializer
from ..models import Team


class TeamListCreateView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
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

    def patch(self, request, *args, **kwargs):
        if self.is_request_valid():
            return self.partial_update(request, *args, **kwargs)

        return self.chief_only_response

    def put(self, request, *args, **kwargs):
        if self.is_request_valid():
            return self.update(request, *args, **kwargs)

        return self.chief_only_response

    def delete(self, request, *args, **kwargs):
        if self.is_request_valid():
            return self.destroy(request, *args, **kwargs)

        return self.chief_only_response


# list (admin) ✅
# get (all) ✅
# create (all) ✅
# update -> name (chiefs) ✅
# delete (chiefs) ✅

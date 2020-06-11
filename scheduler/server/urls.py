from django.urls import path
from .views import TeamListCreateView, TeamDetailView

urlpatterns = [
    path("teams/", TeamListCreateView.as_view(), name="team_list_create"),
    path(
        "teams/<str:name>",
        TeamDetailView.as_view(),
        name="team_retrieve_update_destroy",
    ),
]


# Signup flow
# - Gather credentials
# - Ask to join or create a team
# - if create:
#     - POST -> api/v1/teams -> body: { name }
#     - if !exists -> POST -> api/v1/users -> body: { ...credentials, team_id }
# - if join:
#     - GET -> api/v1/teams/<str:team_name>
#     - if exists -> POST -> api/v1/users -> body: { ...credentials, team_id }

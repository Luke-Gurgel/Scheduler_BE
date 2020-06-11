from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, TeamMemberViewSet


router = DefaultRouter()
router.register(r"teams", TeamViewSet)
router.register(r"team_members", TeamMemberViewSet)

urlpatterns = router.urls

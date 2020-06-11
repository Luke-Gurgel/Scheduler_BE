from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, TeamMemberViewSet, RotationViewSet


router = DefaultRouter()
router.register(r"teams", TeamViewSet)
router.register(r"team_members", TeamMemberViewSet)
router.register(r"rotations", RotationViewSet)

urlpatterns = router.urls

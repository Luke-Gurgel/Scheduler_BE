from rest_framework.routers import DefaultRouter
from .views import (
    TeamViewSet,
    TeamMemberViewSet,
    RotationViewSet,
    ScheduleViewSet,
    ScheduleEntryViewSet,
)


router = DefaultRouter()
router.register(r"teams", TeamViewSet)
router.register(r"team_members", TeamMemberViewSet)
router.register(r"rotations", RotationViewSet)
router.register(r"schedules", ScheduleViewSet)
router.register(r"schedule_entries", ScheduleEntryViewSet)

urlpatterns = router.urls

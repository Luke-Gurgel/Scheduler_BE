from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    TeamViewSet,
    TeamMemberViewSet,
    RotationViewSet,
    ScheduleViewSet,
    ScheduleEntryListCreateView,
    ScheduleEntryUpdateView,
)


router = DefaultRouter()
router.register(r"teams", TeamViewSet)
router.register(r"team_members", TeamMemberViewSet)
router.register(r"rotations", RotationViewSet)
router.register(r"schedules", ScheduleViewSet)

urlpatterns = [
    path("schedules/<int:schedule_id>/entries", ScheduleEntryListCreateView.as_view()),
    path(
        "schedules/<int:schedule_id>/entries/<int:entry_id>",
        ScheduleEntryUpdateView.as_view(),
    ),
]

urlpatterns += router.urls

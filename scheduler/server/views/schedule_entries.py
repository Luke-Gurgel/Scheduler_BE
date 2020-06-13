from datetime import datetime, timedelta
from rest_framework import status
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from ..serializers import ScheduleEntrySerializer
from ..models import Schedule, ScheduleEntry


class ScheduleEntryListCreateView(APIView):
    """API View for creating and listing schedule entries."""

    def get(self, request: Request, schedule_id: int) -> Response:
        """List schedule entries based on date range."""
        if (
            "from_date" not in request.query_params
            or "to_date" not in request.query_params
        ):
            return Response("Request query string missing from_date or to_date param.")

        from_date = datetime.fromisoformat(request.query_params["from_date"])
        to_date = datetime.fromisoformat(request.query_params["to_date"])
        delta = to_date - from_date
        weekly = delta.days > 7
        step = 7 if weekly else 1
        schedule = Schedule.objects.get(pk=schedule_id)
        entries = schedule.scheduleentry_set.filter(
            shift_start_date__range=(from_date, to_date)
        )[::step]
        serializer = ScheduleEntrySerializer(entries, many=True)
        return Response(serializer.data)

    def post(self, request: Request, scheduler_id: int) -> Response:
        """Create one/many schedule entries."""
        if "entries" not in request.data:
            return Response(
                "Missing 'entries' in request body", status=status.HTTP_400_BAD_REQUEST
            )

        entries = request.data["entries"]
        if len(entries) == 0:
            return Response(
                "Entries array cannot be empty", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            serializer = ScheduleEntrySerializer(data=entries, many=True)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        except ValidationError as err:
            return Response(err.messages, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as err:
            return Response(str(err), status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response(str(err), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ScheduleEntryUpdateView(APIView):
    """API View for updating schedule entries."""

    def patch(self, request: Request, schedule_id: int, entry_id: int) -> Response:
        """Update one/many schedule entries."""
        if "mode" not in request.query_params:
            return Response("Request query string is missing 'mode' param.")

        update_mode = request.query_params["mode"]
        entry = None
        try:
            entry = ScheduleEntry.objects.get(pk=entry_id)
        except ObjectDoesNotExist:
            return Response(
                "Specified schedule entry does not exist.",
                status=status.HTTP_404_NOT_FOUND,
            )

        if update_mode == "daily":
            return self.update_one(request, entry)
        elif update_mode == "weekly":
            return self.update_many(request, entry)
        return Response("Unsupported update mode")

    def update_one(self, request, entry):
        serializer = ScheduleEntrySerializer(entry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update_many(self, request, entry):
        end_of_week_date = entry.shift_start_date + timedelta(7)
        ScheduleEntry.objects.filter(
            schedule=entry.schedule,
            team_member=entry.team_member,
            shift_start_date__range=(entry.shift_start_date, end_of_week_date),
        )

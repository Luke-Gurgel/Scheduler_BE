from django.db import models


class Schedule(models.Model):
    team = models.ForeignKey("Team", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.start_date} - {self.end_date}"


class ScheduleEntry(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    rotation = models.ForeignKey("Rotation", on_delete=models.CASCADE)
    author = models.ForeignKey(
        "TeamMember",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entry_author",
        related_query_name="entry_author",
    )
    team_member = models.ForeignKey(
        "TeamMember",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="schedule_entry_team_member",
        related_query_name="schedule_entry_team_member",
    )
    shift_start_date = models.DateTimeField()
    shift_end_date = models.DateTimeField()
    is_backup = models.BooleanField(default=False)
    is_night = models.BooleanField(default=False)
    is_off = models.BooleanField(default=False)
    notes = models.TextField(default="")


class ScheduleChangeRequest(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    author = models.ForeignKey(
        "TeamMember",
        on_delete=models.CASCADE,
        related_name="change_author",
        related_query_name="change_author",
    )
    team_member = models.ForeignKey(
        "TeamMember",
        on_delete=models.CASCADE,
        related_name="schedule_change_request_team_member",
        related_query_name="schedule_change_request_team_member",
    )
    rotation = models.ForeignKey("Rotation", on_delete=models.CASCADE)
    shift_start_date = models.DateTimeField()
    shift_end_date = models.DateTimeField()
    is_backup = models.BooleanField(default=False)
    is_night = models.BooleanField(default=False)
    is_off = models.BooleanField(default=False)
    notes = models.TextField()

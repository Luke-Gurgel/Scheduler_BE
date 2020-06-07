from django.db import models


class Schedule(models.Model):
    team_ref = models.ForeignKey('Team', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.start_date} - {self.end_date}'


class ScheduleEntry(models.Model):
    schedule_ref = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    team_member_id = models.IntegerField()
    rotation_id = models.IntegerField()
    shift_start_date = models.DateTimeField()
    shift_end_date = models.DateTimeField()
    is_backup = models.BooleanField(default=False)
    is_night = models.BooleanField(default=False)
    is_off = models.BooleanField(default=False)
    notes = models.TextField()


class ScheduleChangeRequest(models.Model):
    schedule_ref = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    author_ref = models.ForeignKey('TeamMember', on_delete=models.CASCADE)
    team_member_id = models.IntegerField()
    rotation_id = models.IntegerField()
    shift_start_date = models.DateTimeField()
    shift_end_date = models.DateTimeField()
    is_backup = models.BooleanField(default=False)
    is_night = models.BooleanField(default=False)
    is_off = models.BooleanField(default=False)
    notes = models.TextField()

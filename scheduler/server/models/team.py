from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator


class Team(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)

    def __str__(self):
        return f"{self.name} team"


class TeamMember(models.Model):
    team = models.ForeignKey("Team", on_delete=models.CASCADE)
    fname = models.CharField(max_length=30, null=False)
    lname = models.CharField(max_length=30, null=False)
    email = models.EmailField(max_length=254, unique=True)
    column_order_position = models.PositiveSmallIntegerField()
    year = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(4)]
    )

    def save(self, **kwargs):
        try:
            self.full_clean()
            super(TeamMember, self).save(**kwargs)
        except ValidationError as err:
            print("Validation error:", err)

    @property
    def full_name(self):
        return f"{self.fname} {self.lname}"

    @property
    def is_chief(self):
        return self.year == 4

    def __str__(self):
        return f"{self.full_name}(pgy{self.year}) - member of {self.team.name}"


class Rotation(models.Model):
    team = models.ForeignKey("Team", on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    hex_color = models.CharField(max_length=7)
    num_weeks = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(52)]
    )
    weight = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(3)]
    )

    def save(self, **kwargs):
        try:
            self.full_clean()
            super(Rotation, self).save(**kwargs)
        except ValidationError as err:
            print("Validation error:", err)

    def __str__(self):
        return f"{self.name}"


# Signup flow
# - Gather credentials
# - Ask to join or create a team
# - if create:
#     - POST -> api/v1/teams -> body: { name }
#     - if !exists -> POST -> api/v1/users -> body: { ...credentials, team_id }
# - if join:
#     - GET -> api/v1/teams/<str:team_name>
#     - if exists -> POST -> api/v1/users -> body: { ...credentials, team_id }

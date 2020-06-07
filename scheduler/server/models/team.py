from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
# from django.contrib.postgres import fields


class Team(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)
    # chiefs = fields.ArrayField(base_field=models.IntegerField(), default=list)

    def __str__(self):
        return f'{self.name} team'


class TeamMember(models.Model):
    team_ref = models.ForeignKey('Team', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=30, null=False)
    email = models.EmailField(max_length=254)
    column_order_position = models.IntegerField()
    year = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )

    def save(self, **kwargs):
        try:
            self.full_clean()
            super(TeamMember, self).save(**kwargs)
        except ValidationError as err:
            print('Validation error:', err)

    def __str__(self):
        return f'{self.full_name} (pgy{self.year}) - member of the {self.team_ref.name} team'


class Rotation(models.Model):
    team_ref = models.ForeignKey('Team', on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    hex_color = models.CharField(max_length=7)
    num_weeks = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(52)]
    )
    weight = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(3)]
    )

    def save(self, **kwargs):
        try:
            self.full_clean()
            super(Rotation, self).save(**kwargs)
        except ValidationError as err:
            print('Validation error:', err)

    def __str__(self):
        return f'{self.name}'

# Generated by Django 3.0.7 on 2020-06-06 20:27

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('column_order_position', models.IntegerField()),
                ('year', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('team_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Team')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_member_id', models.IntegerField()),
                ('rotation_id', models.IntegerField()),
                ('shift_start_date', models.DateTimeField()),
                ('shift_end_date', models.DateTimeField()),
                ('is_backup', models.BooleanField(default=False)),
                ('is_night', models.BooleanField(default=False)),
                ('is_off', models.BooleanField(default=False)),
                ('notes', models.TextField()),
                ('schedule_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Schedule')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleChangeRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_member_id', models.IntegerField()),
                ('rotation_id', models.IntegerField()),
                ('shift_start_date', models.DateTimeField()),
                ('shift_end_date', models.DateTimeField()),
                ('is_backup', models.BooleanField(default=False)),
                ('is_night', models.BooleanField(default=False)),
                ('is_off', models.BooleanField(default=False)),
                ('notes', models.TextField()),
                ('author_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.TeamMember')),
                ('schedule_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Schedule')),
            ],
        ),
        migrations.AddField(
            model_name='schedule',
            name='team_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Team'),
        ),
        migrations.CreateModel(
            name='Rotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('hex_color', models.CharField(max_length=7)),
                ('num_weeks', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(52)])),
                ('weight', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(3)])),
                ('team_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Team')),
            ],
        ),
    ]

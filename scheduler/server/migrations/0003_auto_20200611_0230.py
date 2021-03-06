# Generated by Django 3.0.7 on 2020-06-11 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_auto_20200611_0110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teammember',
            name='column_order_position',
            field=models.PositiveSmallIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]

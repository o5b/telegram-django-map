# Generated by Django 5.0.6 on 2024-07-03 15:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0002_alter_marker_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='marker',
            name='user',
            field=models.ForeignKey(limit_choices_to={'is_staff': False}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='markers', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]

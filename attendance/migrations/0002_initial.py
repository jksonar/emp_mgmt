# Generated by Django 5.0.2 on 2025-05-03 18:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('attendance', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attendancecorrection',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_corrections', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attendancecorrection',
            name='attendance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='corrections', to='attendance.attendance'),
        ),
        migrations.AddField(
            model_name='attendancecorrection',
            name='requested_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested_corrections', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together={('employee', 'date')},
        ),
    ]

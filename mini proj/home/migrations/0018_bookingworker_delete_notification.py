# Generated by Django 4.2.5 on 2023-11-21 18:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingWorker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending', max_length=10)),
                ('duration', models.PositiveIntegerField(default=1)),
                ('duration_unit', models.CharField(choices=[('days', 'Days'), ('months', 'Months')], default='days', max_length=10)),
                ('is_work_completed', models.BooleanField(default=False)),
                ('date_requested', models.DateTimeField(auto_now_add=True)),
                ('date_accepted', models.DateTimeField(blank=True, null=True)),
                ('date_declined', models.DateTimeField(blank=True, null=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings_as_agent', to=settings.AUTH_USER_MODEL)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings_as_employer', to=settings.AUTH_USER_MODEL)),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='home.migratoryworker')),
            ],
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
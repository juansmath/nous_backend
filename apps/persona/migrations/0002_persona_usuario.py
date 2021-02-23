# Generated by Django 3.1.5 on 2021-02-19 05:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('persona', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
# Generated by Django 4.2.6 on 2024-01-06 14:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Accommodationdetailstable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('district', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=255)),
                ('lowest_rate', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('highest_rate', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('restaurant', models.BooleanField(blank=True, default=False, null=True)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='accommodation_images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
# Generated by Django 5.1.3 on 2024-12-10 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniapp', '0015_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='company_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='resumes/'),
        ),
        migrations.AddField(
            model_name='profile',
            name='skills',
            field=models.TextField(blank=True, null=True),
        ),
    ]

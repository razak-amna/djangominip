# Generated by Django 5.1.3 on 2024-12-03 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miniapp', '0002_application_status_jobseeker_skills_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='application',
            old_name='job_seeker',
            new_name='jobseeker',
        ),
    ]

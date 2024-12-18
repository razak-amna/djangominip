# Generated by Django 5.1.3 on 2024-12-07 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniapp', '0008_alter_customuser_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recruiters',
            name='company_description',
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='achievements',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='certificates',
            field=models.FileField(blank=True, null=True, upload_to='certificates/'),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='contact',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='phone',
            field=models.CharField(default=1234567890, max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='qualifications',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='recruiters',
            name='contact',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recruiters',
            name='job_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recruiters',
            name='job_title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='recruiters',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='recruiters',
            name='salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='recruiters',
            name='skills_required',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='experience',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='recruiters',
            name='company_logo',
            field=models.ImageField(blank=True, null=True, upload_to='logos/'),
        ),
        migrations.AlterField(
            model_name='recruiters',
            name='company_name',
            field=models.CharField(max_length=200),
        ),
    ]
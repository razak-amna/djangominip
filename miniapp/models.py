from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Recruiters(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruiter_profile')
    company_name = models.CharField(max_length=200)
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    contact = models.TextField(null=True, blank=True)
    skills_required = models.TextField(null=True, blank=True)
    job_title = models.CharField(max_length=200, null=True, blank=True)
    job_description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.company_name

    def email(self):
        return self.user.email


class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='jobseeker_profile')
    phone = models.CharField(max_length=15)
    contact = models.TextField(null=True, blank=True)
    qualifications = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    certificates = models.FileField(upload_to='certificates/', null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    achievements = models.TextField(null=True, blank=True)
    experience = models.CharField(max_length=100, null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def email(self):
        return self.user.email


class Job(models.Model):
    recruiter = models.ForeignKey('Recruiters', on_delete=models.CASCADE, related_name='jobs_posted', verbose_name='Company')
    title = models.CharField(max_length=200, verbose_name='Job Title')
    description = models.TextField(verbose_name='Description')
    skills_needed = models.TextField(verbose_name='Skills')
    location = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('recruiter', 'title')  # Ensure no duplicate jobs from the same recruiter


class Application(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
    ]
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    jobseeker = models.ForeignKey('JobSeeker', on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.jobseeker.user.username} -> {self.job.title}"

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('jobseeker', 'JobSeeker'),
        ('recruiter', 'Recruiters'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

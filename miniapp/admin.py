from django.contrib import admin
from django.contrib.auth.models import User  # Importing the default User model
from .models import Recruiters, JobSeeker, Job, Application

# Admin for Recruiters model
class RecruitersAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'user_email', 'company_logo')
    search_fields = ('user__username', 'company_name', 'user__email')
    list_filter = ('user__is_active', )
    ordering = ('company_name',)

    def user_email(self, obj):
        return obj.user.email  # Accessing the related User's email field
    user_email.short_description = 'Email'  # For a better column header in admin

# Admin for JobSeeker model
class JobSeekerAdmin(admin.ModelAdmin):
    list_display = ('user', 'resume', 'user_email')
    search_fields = ('user__username', 'user__email')
    list_filter = ('user__is_active',)
    ordering = ('user__username',)

    def user_email(self, obj):
        return obj.user.email  
    user_email.short_description = 'Email' 

# Admin for Job model
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'recruiter', 'location', 'salary', 'posted_at', 'skills_needed')
    search_fields = ('title', 'recruiter__company_name', 'location')
    list_filter = ('location', 'posted_at')
    ordering = ('-posted_at',)
    readonly_fields = ('posted_at',)

# Admin for Application model
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'jobseeker', 'applied_at', 'status')
    search_fields = ('job__title', 'jobseeker__user__username')
    list_filter = ('applied_at', 'status')
    ordering = ('-applied_at',)
    readonly_fields = ('applied_at',)

# Admin for User (CustomUser replaced by default User model)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'is_job_seeker', 'is_recruiter')
#     search_fields = ('username', 'email')
#     list_filter = ('is_active',)
#     ordering = ('username',)

#     def is_job_seeker(self, obj):
#         return hasattr(obj, 'jobseeker')  # Check if the user has a related JobSeeker profile
#     is_job_seeker.boolean = True
#     is_job_seeker.short_description = 'Job Seeker'

#     def is_recruiter(self, obj):
#         return hasattr(obj, 'recruiters')  # Check if the user has a related Recruiter profile
#     is_recruiter.boolean = True
#     is_recruiter.short_description = 'Recruiter'

# # Register the models in the admin site
# admin.site.unregister(User)  # Unregister the default User admin
# admin.site.register(User, UserAdmin)  # Register the default User model with custom admin

admin.site.register(Recruiters, RecruitersAdmin)
admin.site.register(JobSeeker, JobSeekerAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Application, ApplicationAdmin)

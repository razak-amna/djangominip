from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password/<str:username>/', views.reset_password, name='reset-password'),
    path('register/', views.register, name='register'),
    path('jobs/', views.jobs, name='jobs'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('recruiter-dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('post-job/', views.post_job, name='post_job'),
    path('job/<int:job_id>/', views.view_job, name='view_job'),
    path('job/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('job/<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('job/<int:job_id>/apply/', views.apply_for_job, name='apply_for_job'),
    path('profile/', views.profile, name='profile'),
    path('profile/modify/<str:user_type>/', views.modify_profile, name='modify-profile'),
    path('view-resume/<int:jobseeker_id>/', views.view_resume, name='view-resume'),
    path('upload-resume/', views.upload_resume, name='upload-resume'),
    path('upload-logo/', views.upload_company_logo, name='upload-logo'),
    path('apply-job/<int:job_id>/', views.apply_job, name='apply-job'),

]


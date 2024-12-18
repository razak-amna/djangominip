from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password/<str:username>/', views.reset_password, name='reset-password'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
    path('jobs/', views.jobs, name='jobs'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('recruiter-dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('post-job/', views.post_job, name='post_job'),
    path('profile/', views.profile, name='profile'),
    path('modify-jobseeker-profile/', views.modify_jobseeker_profile, name='modify-jobseeker-profile'),
    path('modify-recruiter-profile/', views.modify_recruiter_profile, name='modify-recruiter-profile'),
    path('view-resume/<int:jobseeker_id>/', views.view_resume, name='view-resume'),
    path('upload-resume/', views.upload_resume, name='upload-resume'),
    path('upload-logo/', views.upload_company_logo, name='upload-logo'),
    path('apply-job/<int:job_id>/', views.apply_job, name='apply-job'),

]


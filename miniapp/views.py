from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User, Group
from .forms import UserRegistrationForm, JobSeekerForm, RecruitersForm, ForgotPasswordForm, ResetPasswordForm, PostJobForm
from .models import JobSeeker, Recruiters, Job, Application, Profile

def home(request):
    user_groups = request.user.groups.values_list('name', flat=True)  # Get group names
    is_jobseeker = 'JobSeeker' in user_groups
    is_recruiter = 'Recruiters' in user_groups

    return render(request, 'home.html', {
        'is_jobseeker': is_jobseeker,
        'is_recruiter': is_recruiter,
    })


def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')  # Get the role from the form
        print(request.POST)
        print("Username/Email:", username_or_email)
        print("Role:", role)

        # Authenticate user by username or email
        user = authenticate(request, username=username_or_email, password=password)
        if user is not None:
            # Determine role by checking related models
            if role == 'jobseeker' and JobSeeker.objects.filter(user=user).exists():
                login(request, user)
                return redirect('profile')
            elif role == 'recruiter' and Recruiters.objects.filter(user=user).exists():
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, "Invalid role selected or user does not match the selected role.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username/email or password.")
            return redirect('login')

    return render(request, 'registration/login.html')

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
                # Redirect to password reset page
                return redirect('reset-password', username=user.username)
            except User.DoesNotExist:
                messages.error(request, "Username not found.")
    else:
        form = ForgotPasswordForm()
    return render(request, 'registration/forgot_password.html', {'form': form})

def reset_password(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, "Invalid username.")
        return redirect('forgot-password')

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            # Set the new password
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()

            # Authenticate the user and log them in
            user = authenticate(username=user.username, password=new_password)
            if user is not None:
                login(request, user)
                messages.success(request, "Password reset successfully!")
                return redirect('login')  # Redirect to login page after successful reset
    else:
        form = ResetPasswordForm()

    return render(request, 'reset_password.html', {'form': form, 'username': username})


@login_required
def register(request):
    if request.method == 'POST':
        print("POST request received")
        
        # Fetch and validate user role
        user_role = request.POST.get('user_type')
        if user_role not in ['jobseeker', 'recruiter']:
            print("Invalid role selected")
            return HttpResponseBadRequest("Invalid role selected.")
        
        # Initialize forms
        user_form = UserRegistrationForm(request.POST)
        jobseeker_form = JobSeekerForm(request.POST, request.FILES) if user_role == 'jobseeker' else JobSeekerForm()
        recruiter_form = RecruitersForm(request.POST, request.FILES) if user_role == 'recruiter' else RecruitersForm()

        if user_form.is_valid():
            try:
                # Save the user
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()

                # Assign user to "Users" group
                users_group = Group.objects.get(name='Users')
                user.groups.add(users_group)

                # Handle specific roles
                if user_role == 'jobseeker' and jobseeker_form.is_valid():
                    jobseeker = jobseeker_form.save(commit=False)
                    jobseeker.user = user
                    jobseeker.save()
                    
                    # Automatically create a Profile object if needed
                    Profile.objects.create(user=user, user_type='jobseeker')
                    jobseeker_group = Group.objects.get(name='JobSeeker')
                    user.groups.add(jobseeker_group)

                    messages.success(request, "JobSeeker registered successfully!")
                    return redirect('login')

                elif user_role == 'recruiter' and recruiter_form.is_valid():
                    recruiter = recruiter_form.save(commit=False)
                    recruiter.user = user
                    recruiter.save()

                    Profile.objects.create(user=user, user_type='recruiter')
                    recruiter_group = Group.objects.get(name='Recruiters')
                    user.groups.add(recruiter_group)

                    messages.success(request, "Recruiter registered successfully!")
                    return redirect('login')

                else:
                    print("Profile form errors")
                    messages.error(request, "Please correct the errors in the profile form.")

            except IntegrityError as e:
                print(f"IntegrityError: {e}")
                user_form.add_error('username', "This username is already taken.")
            except Exception as e:
                print(f"Unexpected error: {e}")
                messages.error(request, "An unexpected error occurred. Please try again.")
        else:
            print("User form is invalid")
            print(user_form.errors)

        # If validation fails, render the form again
        return render(request, 'registration/register.html', {
            'form': user_form,
            'jobseeker_form': jobseeker_form,
            'recruiter_form': recruiter_form,
        })

    else:
        # Handle GET requests
        print("GET request received")
        user_form = UserRegistrationForm()
        jobseeker_form = JobSeekerForm()
        recruiter_form = RecruitersForm()

    return render(request, 'registration/register.html', {
        'form': user_form,
        'jobseeker_form': jobseeker_form,
        'recruiter_form': recruiter_form,
    })


@login_required
def jobs(request):
    jobs = Job.objects.all()
    context = {
        'jobs': jobs
    }
    jobs = Job.objects.all()
    for job in jobs:
        print(f"Job Title: {job.title}")
        print(f"Skills Required: {job.skills_needed}")
        print(f"Recruiter: {job.recruiter.company_name if job.recruiter else 'No recruiter'}")
    return render(request, 'registration/jobs.html', {'jobs': jobs})


def user_dashboard(request):
    # Check the user's group membership
    if request.user.groups.filter(name="JobSeeker").exists():
        # Data specifically for Job Seekers
        context = {
            'user_type': 'JobSeeker',
            'dashboard_title': 'Job Seeker Dashboard',
            'dashboard_message': 'Explore job opportunities and manage your applications.',
            'action_url': 'jobs',  # URL name for exploring jobs
            'action_label': 'Explore Jobs',
        }
    elif request.user.groups.filter(name="Recruiters").exists():
        # Data specifically for Recruiters
        context = {
            'user_type': 'Recruiter',
            'dashboard_title': 'Recruiter Dashboard',
            'dashboard_message': 'Post job openings and review applications.',
            'action_url': 'post_job',  # URL name for posting jobs
            'action_label': 'Post a Job',
        }
    else:
        # Default for users without a specific group
        context = {
            'user_type': 'General User',
            'dashboard_title': 'User Dashboard',
            'dashboard_message': 'Access features tailored to your needs.',
            'action_url': 'register',  # URL name for registering
            'action_label': 'Register Now',
        }

    return render(request, 'registration/dashboard.html', context)


@login_required
def recruiter_dashboard(request):
    return render(request, 'recruiter_dashboard.html')


def post_job(request):
    if request.method == 'POST':
        form = PostJobForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Job posted successfully!")
            return redirect('recruiter_dashboard')  # Replace with your desired redirect
        else:
            messages.error(request, "Failed to post the job. Please correct the errors below.")
    else:
        form = PostJobForm()
    return render(request, 'registration/post_job.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    print(f"Rendering profile for: {user.username}")

    try:
        profile = Profile.objects.get(user=request.user)
        print(f"Profile found: {profile}")
        print(f"User Type: {profile.user_type}")
    except Profile.DoesNotExist:
        # Redirect to a profile creation form
        messages.error(request, "No profile found. Please complete your profile.")
        return redirect('modify-jobseeker-profile' if user.groups.filter(name='JobSeeker').exists() else 'modify-recruiter-profile')
    print(f"User type: {profile.user_type}")

    if profile.user_type == 'jobseeker':
        try:
            jobseeker_profile = JobSeeker.objects.prefetch_related('applications__job').get(user=request.user)
            return render(request, 'registration/profile.html', {'profile': jobseeker_profile})
        except JobSeeker.DoesNotExist:
            messages.error(request, "JobSeeker profile not found. Please update your profile.")
            return redirect('modify-jobseeker-profile')

    elif profile.user_type == 'recruiter':
        try:
            recruiter_profile = Recruiters.objects.prefetch_related('jobs_posted__applications').get(user=request.user)
            return render(request, 'registration/profile.html', {'profile': recruiter_profile})
        except Recruiters.DoesNotExist:
            messages.error(request, "Recruiter profile not found. Please update your profile.")
            return redirect('modify-recruiter-profile')
        print(request)
    else:
        return HttpResponse("User role not recognized.")

@login_required
def modify_jobseeker_profile(request):
    user = request.user
    print(f"Rendering modify profile for: {user.username}")

    try:
        jobseeker_profile = JobSeeker.objects.get(user=request.user)
    except JobSeeker.DoesNotExist:
        # Handle the case when the JobSeeker profile does not exist
        jobseeker_profile = None
        print("No job seeker profile found")

    if request.method == 'POST':
        form = JobSeekerForm(request.POST, request.FILES, instance=jobseeker_profile)
        if form.is_valid():
            form.save()
            print("Form saved successfully")

            # Redirect to profile page after save
            return HttpResponseRedirect('/profile/')  # Direct URL to profile

        else:
            print(f"Form errors: {form.errors}")
    else:
        form = JobSeekerForm(instance=jobseeker_profile)

    return render(request, 'registration/modify_jobseeker_profile.html', {'form': form})

@login_required
def modify_recruiter_profile(request):
    recruiter_profile = get_object_or_404(Recruiters, user=request.user)
    try:
        # Access the Recruiter profile
        recruiter = request.user.recruiter_profile  # Use 'recruiter_profile' if related_name is set
    except Recruiters.DoesNotExist:
        # If no recruiter profile exists, create one
        recruiter = Recruiters(user=request.user)
        recruiter.save()

    if request.method == 'POST':
        form = RecruitersForm(request.POST, instance=recruiter_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')  # Redirect to the correct profile view
    else:
        form = RecruitersForm(instance=recruiter)
    
    return render(request, 'registration/modify_recruiter_profile.html', {'form': form})



@login_required
def upload_resume(request):
    # Fetch the JobSeeker object for the logged-in user (use request.user to refer to the logged-in user)
    jobseeker, created = JobSeeker.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = JobSeekerForm(request.POST, request.FILES, instance=jobseeker)
        if form.is_valid():
            form.save()
            return HttpResponse("Resume uploaded successfully!")
    else:
        form = JobSeekerForm(instance=jobseeker)

    return render(request, 'registration/upload_resume.html', {'form': form})


@login_required
def upload_company_logo(request):
    # Fetch the Recruiters object for the logged-in user
    recruiter, created = Recruiters.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = RecruitersForm(request.POST, request.FILES, instance=recruiter)
        if form.is_valid():
            form.save()
            return HttpResponse("Company Logo uploaded successfully!")
    else:
        form = RecruitersForm(instance=recruiter)

    return render(request, 'registration/upload_logo.html', {'form': form})

@login_required
def view_resume(request, jobseeker_id):
    # Get the JobSeeker object or 404 if not found
    jobseeker = get_object_or_404(JobSeeker, id=jobseeker_id)

    # Check if the user has permission to view the resume
    # You can add your own logic here to check if the user is allowed
    if not request.user.is_authenticated:
        return redirect('login')

    context = {
        'jobseeker': jobseeker,
    }
    return render(request, 'registration/view_resume.html', context)


@login_required
def apply_job(request, job_id):
    try:
        job = get_object_or_404(Job, id=job_id)
    except Job.DoesNotExist:
        messages.error(request, "The specified job does not exist.")
        return redirect('jobs')

    if not JobSeeker.objects.filter(user=request.user).exists():
        messages.error(request, "You need to be a job seeker to apply for a job.")
        return redirect('jobs')

    jobseeker = JobSeeker.objects.get(user=request.user)

    if request.method == 'POST':
        cover_letter = request.POST.get('cover_letter', '')
        try:
            Application.objects.create(job=job, jobseeker=jobseeker, cover_letter=cover_letter)
            messages.success(request, "Job applied successfully! Search for another job.")
        except Exception as e:
            messages.error(request, f"An error occurred while submitting your application: {str(e)}")
        return redirect('jobs')

    return render(request, 'registration/apply_job.html', {'job': job})

from django import forms
from django.contrib.auth.models import User
from .models import JobSeeker, Recruiters , Profile, Job


class UserRegistrationForm(forms.ModelForm):
    #Form for registering a user with username, email, and password.
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label="Confirm Password"
    )
    user_type = forms.ChoiceField(choices=Profile.USER_TYPE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_type']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username

    def clean(self):
        #Ensure password and confirm password match.
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Profile.objects.create(user=user, user_type=self.cleaned_data['user_type'])
        return user


class JobSeekerForm(forms.ModelForm):
    #Form for additional JobSeeker profile details.
    class Meta:
        model = JobSeeker
        fields = [
            'phone', 'contact', 'qualifications',
            'skills', 'certificates', 'resume', 'achievements',
            'experience', 'salary'
        ]
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}),
            'qualifications': forms.TextInput(attrs={'placeholder': 'Enter Qualifications'}),
            'skills': forms.Textarea(attrs={'placeholder': 'Enter Skills'}),
        }


class RecruitersForm(forms.ModelForm):
    #Form for additional Recruiter profile details.
    class Meta:
        model = Recruiters
        fields = [
            'company_name', 'company_logo', 'contact',
            'skills_required', 'job_title', 'job_description',
            'location', 'salary'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'placeholder': 'Enter Company Name'}),
            'skills_required': forms.Textarea(attrs={'placeholder': 'Enter Required Skills'}),
        }

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'recruiter','location', 'skills_needed', 'description', 'salary']


class PostJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'salary', 'recruiter', 'skills_needed']


class ForgotPasswordForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(), label='New Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
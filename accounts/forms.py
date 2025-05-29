from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import ContractorProfile, WorkerProfile, JobPost, SubWorker, JobApplication, Rating
from django.core.exceptions import ValidationError
from datetime import date


User = get_user_model() 

class UserRegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES)
    full_name = forms.CharField(max_length=100)
    contact_number = forms.CharField(max_length=17)
    age = forms.IntegerField(required=False, min_value=18, max_value=100)
    gender = forms.ChoiceField(choices=User._meta.get_field('gender').choices, required=False)
    email = forms.EmailField(max_length=100, required=True)
    city = forms.CharField(max_length=100, required=True)
    
    class Meta:
        model = User
        fields = ['user_type', 'full_name', 'contact_number', 'age', 'gender', 'email', 'city', 'username', 'password1', 'password2']
    
    def clean_contact_number(self):
        contact_number = self.cleaned_data['contact_number']
        if not contact_number.startswith('+'):
            raise ValidationError("Contact number must start with '+'.")
        if User.objects.filter(contact_number=contact_number).exclude(id=self.instance.id).exists():
            raise ValidationError("This contact number is already registered.")
        return contact_number
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_city(self):
        city = self.cleaned_data['city']
        if len(city) < 2:
            raise ValidationError("City name must be at least 2 characters long.")
        return city

class ContractorProfileForm(forms.ModelForm):
    class Meta:
        model = ContractorProfile
        fields = ['address', 'profile_image']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class WorkerProfileForm(forms.ModelForm):
    class Meta:
        model = WorkerProfile
        fields = ['address', 'profile_image']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'location', 'description', 'requirements', 'eligibility', 'worker_count', 'duration', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
            'eligibility': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        worker_count = cleaned_data.get('worker_count')
        if start_date and end_date and end_date < start_date:
            raise ValidationError("End date must be after start date.")
        if start_date and start_date < date.today():
            raise ValidationError("Start date cannot be in the past.")
        if worker_count and worker_count < 1:
            raise ValidationError("Number of workers must be at least 1.")
        return cleaned_data

class SubWorkerForm(forms.ModelForm):
    class Meta:
        model = SubWorker
        fields = ['full_name', 'contact_number', 'age', 'gender', 'skills']
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_contact_number(self):
        contact_number = self.cleaned_data['contact_number']
        if not contact_number.startswith('+'):
            raise ValidationError("Contact number must start with '+'.")
        return contact_number

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add a cover letter (optional)'})
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating_value', 'comment']
        widgets = {
            'rating_value': forms.Select(choices=[(i, str(i)) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add your feedback (optional)'}),
        }
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError


phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

class User(AbstractUser):
    USER_TYPE_CHOICES= (
        ('worker', 'Worker'),
        ('contractor', 'Contractor'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='worker')
    full_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=17, validators=[phone_regex])
    age = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(18), MaxValueValidator(100)]
    )
    
    gender = models.CharField(
        max_length=20,
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other'),
            ('not added', 'Prefer not to say')
        ],
        default='not added'
    )
    skills_description = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=False, default='Not specified')

    class Meta:
        ordering = ['full_name']
    
    def __str__(self):
        return self.full_name
    
class ContractorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='contractorprofile')
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.full_name}'s Contractor Profile"

class WorkerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='workerprofile')
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.full_name}'s Worker Profile"

class SubWorker(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subworkers')
    full_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=17, validators=[phone_regex])
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(100)]
    )
    gender = models.CharField(max_length=20, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ])
    skills = models.TextField()
    
    def __str__(self):
        return self.full_name

class JobPost(models.Model):
    contractor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobposts')
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    eligibility = models.TextField()
    worker_count = models.PositiveIntegerField()
    duration = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return self.title

class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    applied_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['job', 'worker']
    
    def __str__(self):
        return f"{self.worker.full_name}'s application for {self.job.title}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return self.message


class Rating(models.Model):
    RATING_TYPE_CHOICES = (
        ('worker_to_contractor', 'Worker to Contractor'),
        ('contractor_to_worker', 'Contractor to Worker'),
        ('worker_to_job', 'Worker to Job'),
    )
    
    rating_type = models.CharField(max_length=20, choices=RATING_TYPE_CHOICES)
    rating_value = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_ratings', null=True, blank=True)
    target_job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='ratings', null=True, blank=True)
    
    class Meta:
        # Single unique_together constraint that includes all relevant fields
        unique_together = [['reviewer', 'target_user', 'target_job', 'rating_type']]
    
    def clean(self):
        # Validation to ensure correct usage of target_user and target_job
        if self.rating_type in ('worker_to_contractor', 'contractor_to_worker'):
            if not self.target_user:
                raise ValidationError("target_user must be set for worker_to_contractor or contractor_to_worker ratings.")
            if self.target_job:
                raise ValidationError("target_job must be null for worker_to_contractor or contractor_to_worker ratings.")
        elif self.rating_type == 'worker_to_job':
            if not self.target_job:
                raise ValidationError("target_job must be set for worker_to_job ratings.")
            if self.target_user:
                raise ValidationError("target_user must be null for worker_to_job ratings.")
    
    def save(self, *args, **kwargs):
        # Run validation before saving
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        if self.rating_type == 'worker_to_job':
            return f"{self.reviewer.full_name}'s rating for {self.target_job.title}"
        return f"{self.reviewer.full_name}'s rating for {self.target_user.full_name}"
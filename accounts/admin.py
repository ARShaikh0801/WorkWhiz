from django.contrib import admin
from .models import User, ContractorProfile, WorkerProfile, SubWorker, JobPost, JobApplication, Notification, Rating

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user_type', 'contact_number', 'city', 'is_active')
    list_filter = ('user_type', 'city', 'is_active')
    search_fields = ('full_name', 'contact_number', 'email', 'username')
    list_per_page = 25

@admin.register(ContractorProfile)
class ContractorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address')
    search_fields = ('user__full_name', 'address')
    list_per_page = 25

@admin.register(WorkerProfile)
class WorkerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address')
    search_fields = ('user__full_name', 'address')
    list_per_page = 25

@admin.register(SubWorker)
class SubWorkerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'worker', 'contact_number', 'age')
    list_filter = ('gender',)
    search_fields = ('full_name', 'worker__full_name', 'contact_number')
    list_per_page = 25

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'contractor', 'location', 'date_posted', 'start_date', 'end_date')
    list_filter = ('location', 'date_posted', 'start_date')
    search_fields = ('title', 'contractor__full_name', 'location')
    list_per_page = 25

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'worker', 'status', 'applied_date')
    list_filter = ('status', 'applied_date')
    search_fields = ('job__title', 'worker__full_name')
    list_per_page = 25

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('message', 'user__full_name')
    list_per_page = 25

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'rating_type', 'rating_value', 'created_at')
    list_filter = ('rating_type', 'created_at')
    search_fields = ('reviewer__full_name', 'target_user__full_name', 'target_job__title')
    list_per_page = 25
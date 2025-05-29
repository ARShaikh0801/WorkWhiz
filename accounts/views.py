from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .forms import UserRegistrationForm, ContractorProfileForm, WorkerProfileForm, JobPostForm, SubWorkerForm, JobApplicationForm, RatingForm
from .models import User, ContractorProfile, WorkerProfile, SubWorker, JobPost, JobApplication, Notification, Rating
from django.utils import timezone
from datetime import datetime, timedelta
import json
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db import models
from django.db.models import Avg

def index(request):
    if request.method == 'POST' and 'language' in request.POST:
        request.session['language'] = request.POST['language']
    language = request.session.get('language', 'en')
    return render(request, 'index.html', {'language': language})

def sign_up(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.user_type == 'contractor':
                ContractorProfile.objects.create(user=user, city=user.city)
            else:
                WorkerProfile.objects.create(user=user, city=user.city)
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('accounts:log_in')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()
    language = request.session.get('language', 'en')
    return render(request, 'sign_up.html', {'form': form, 'language': language})

def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == 'contractor':
                return redirect('accounts:contractor_dashboard')
            else:
                return redirect('accounts:worker_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    language = request.session.get('language', 'en')
    return render(request, 'log_in.html', {'language': language})

def log_out(request):
    logout(request)
    return redirect('accounts:index')

def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                reverse('accounts:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_url}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Password reset link sent to your email.')
            return redirect('accounts:password_reset_done')
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email.')
    language = request.session.get('language', 'en')
    return render(request, 'accounts/forget_password.html', {'language': language})

def password_reset_complete(request):
    language = request.session.get('language', 'en')
    messages.success(request, 'Your password has been successfully reset. You can now log in.')
    return render(request, 'accounts/password_reset_complete.html', {'language': language})

@login_required
def contractor_dashboard(request):
    workers = WorkerProfile.objects.all()
    jobs = JobPost.objects.filter(contractor=request.user)
    for worker in workers:
        worker.average_rating = Rating.objects.filter(target_user=worker.user, rating_type='contractor_to_worker').aggregate(models.Avg('rating_value'))['rating_value__avg'] or 0

    job_applications = JobApplication.objects.filter(job__contractor=request.user).select_related('worker', 'job')
    language = request.session.get('language', 'en')
    return render(request, 'accounts/contractor_dashboard.html', {
        'workers': workers,
        'jobs': jobs,
        'job_applications': job_applications,
        'user_profile': request.user,
        'today': timezone.now().date(),
        'language': language
    })

@login_required
def worker_dashboard(request):
    jobs = JobPost.objects.filter(end_date__gte=timezone.now().date())
    applications = JobApplication.objects.filter(worker=request.user)
    subworkers = SubWorker.objects.filter(worker=request.user)
    
    city = request.user.city.lower() if request.user.city else ''
    if request.GET.get('location') == 'worker' and city:
        jobs = jobs.filter(location__icontains=city)
    
    for job in jobs:
        job.average_rating = Rating.objects.filter(target_job=job, rating_type='worker_to_job').aggregate(models.Avg('rating_value'))['rating_value__avg'] or 0
        job.contractor_rating = Rating.objects.filter(target_user=job.contractor, rating_type='worker_to_contractor').aggregate(models.Avg('rating_value'))['rating_value__avg'] or 0
    
    language = request.session.get('language', 'en')
    return render(request, 'accounts/worker_dashboard.html', {
        'jobs': jobs,
        'applications': applications,
        'subworkers': subworkers,
        'user_profile': request.user,
        'profile': request.user.workerprofile,
        'language': language
    })

@login_required
def contractor_profile(request):
    profile, created = ContractorProfile.objects.get_or_create(user=request.user, defaults={'city': request.user.city})
    if request.method == 'POST':
        form = ContractorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:contractor_dashboard')
        else:
            messages.error(request, 'Error updating profile.')
    else:
        form = ContractorProfileForm(instance=profile)
    average_rating = Rating.objects.filter(target_user=request.user, rating_type='worker_to_contractor').aggregate(models.Avg('rating_value'))['rating_value__avg'] or 0
    language = request.session.get('language', 'en')
    return render(request, 'accounts/contractor_profile.html', {
        'form': form,
        'profile': profile,
        'user_profile': request.user,
        'average_rating': average_rating,
        'language': language
    })

@login_required
def worker_profile(request):
    # Restrict access to workers only
    if request.user.user_type != 'worker':
        messages.error(request, 'Only workers can access this page.')
        return redirect('accounts:worker_dashboard')

    # Get or create the worker profile
    profile, created = WorkerProfile.objects.get_or_create(user=request.user, defaults={'city': request.user.city})
    subworkers = SubWorker.objects.filter(worker=request.user)  # Fetch subworkers for the table

    if request.method == 'POST':
        if 'add_subworker' in request.POST:
            subworker_form = SubWorkerForm(request.POST)
            if subworker_form.is_valid():
                subworker = subworker_form.save(commit=False)
                subworker.worker = request.user
                subworker.save()
                messages.success(request, 'Team member added successfully.')
                return redirect('accounts:worker_profile')
            else:
                messages.error(request, 'Error adding team member.')
                # Keep the form with errors to display specific field errors in the template
        elif 'profile_image' in request.FILES:
            # Basic validation for profile image
            profile_image = request.FILES['profile_image']
            if profile_image.size > 5 * 1024 * 1024:  # Limit to 5MB
                messages.error(request, 'Profile image must be under 5MB.')
                return redirect('accounts:worker_profile')
            if not profile_image.content_type.startswith('image/'):
                messages.error(request, 'Profile image must be an image file.')
                return redirect('accounts:worker_profile')
            profile.profile_image = profile_image
            profile.save()
            messages.success(request, 'Profile image updated successfully.')
            return redirect('accounts:worker_profile')
    else:
        subworker_form = SubWorkerForm()

    # Calculate average rating
    average_rating = Rating.objects.filter(
        target_user=request.user, rating_type='contractor_to_worker'
    ).aggregate(Avg('rating_value'))['rating_value__avg'] or 0

    language = request.session.get('language', 'en')
    return render(request, 'accounts/worker_profile.html', {
        'subworker_form': subworker_form,
        'profile': profile,
        'user_profile': request.user,
        'average_rating': average_rating,
        'subworkers': subworkers,  # Add subworkers to context
        'language': language,
    })
@login_required
def edit_profile(request):
    profile = request.user.contractorprofile if request.user.user_type == 'contractor' else request.user.workerprofile
    form_class = ContractorProfileForm if request.user.user_type == 'contractor' else WorkerProfileForm
    
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            request.user.full_name = request.POST.get('full_name')
            request.user.contact_number = request.POST.get('contact_number')
            request.user.age = request.POST.get('age') or None
            request.user.gender = request.POST.get('gender')
            request.user.skills_description = request.POST.get('skills_description')
            request.user.city = request.POST.get('city')
            profile.city = request.user.city
            
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if current_password and new_password:
                if new_password != confirm_password:
                    messages.error(request, 'New passwords do not match.')
                    return redirect('accounts:edit_contractor_profile' if request.user.user_type == 'contractor' else 'accounts:edit_worker_profile')
                if request.user.check_password(current_password):
                    request.user.set_password(new_password)
                    messages.success(request, 'Password updated successfully.')
                else:
                    messages.error(request, 'Current password is incorrect.')
                    return redirect('accounts:edit_contractor_profile' if request.user.user_type == 'contractor' else 'accounts:edit_worker_profile')
            
            request.user.save()
            profile.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:contractor_profile' if request.user.user_type == 'contractor' else 'accounts:worker_profile')
        else:
            messages.error(request, 'Error updating profile.')
    else:
        form = form_class(instance=profile)
    
    language = request.session.get('language', 'en')
    return render(request, 'edit_profile.html', {
        'form': form,
        'language': language,
        'user_profile': request.user
    })
@login_required
def post_job(request):
    if not request.user.city or not request.user.skills_description:
        messages.error(request, 'Please complete your profile before posting a job.')
        return redirect('accounts:edit_contractor_profile')
    
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.contractor = request.user
            job.save()
            messages.success(request, 'Job posted successfully.')
            return redirect('accounts:contractor_dashboard')
        else:
            messages.error(request, 'Error posting job.')
    else:
        form = JobPostForm()
    language = request.session.get('language', 'en')
    return render(request, 'accounts/post-job.html', {'form': form, 'form_errors': form.errors, 'language': language})

@login_required
def my_jobs(request):
    jobs = JobPost.objects.filter(contractor=request.user)
    for job in jobs:
        job.average_rating = Rating.objects.filter(target_job=job, rating_type='worker_to_job').aggregate(models.Avg('rating_value'))['rating_value__avg'] or 0
    language = request.session.get('language', 'en')
    return render(request, 'accounts/my-jobs.html', {'jobs': jobs, 'today': timezone.now().date(), 'language': language})

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id, contractor=request.user)
    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully.')
            return redirect('accounts:my_jobs')
        else:
            messages.error(request, 'Invalid form data.')
            return redirect('accounts:my_jobs')
    return HttpResponseBadRequest()

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id, contractor=request.user)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully.')
        return redirect('accounts:my_jobs')
    messages.error(request, 'Invalid request.')
    return redirect('accounts:my_jobs')

@login_required
def get_job_details(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    average_rating = Rating.objects.filter(target_job=job, rating_type='worker_to_job').aggregate(models.Avg('rating_value'))['rating_value__avg'] or 0
    data = {
        'title': job.title,
        'location': job.location,
        'description': job.description,
        'requirements': job.requirements,
        'eligibility': job.eligibility,
        'worker_count': job.worker_count,
        'duration': job.duration,
        'start_date': job.start_date.isoformat(),
        'end_date': job.end_date.isoformat(),
        'contractor': job.contractor.full_name,
        'average_rating': average_rating
    }
    return JsonResponse(data)

@login_required
def submit_application(request, job_id):
    if not request.user.city or not request.user.skills_description:
        messages.error(request, 'Please complete your profile before applying.')
        return redirect('accounts/worker_profile.html')
    
    job = get_object_or_404(JobPost, id=job_id)
    if JobApplication.objects.filter(job=job, worker=request.user).exists():
        messages.error(request, 'You have already applied for this job.')
        return redirect('accounts/worker_dashboard.html')
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.worker = request.user
            application.save()
            
            Notification.objects.create(
                user=job.contractor,
                message=f"New application from {request.user.full_name} for {job.title}"
            )
            
            return JsonResponse({'status': 'success', 'message': 'Application submitted successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Error submitting application.', 'errors': form.errors}, status=400)
    return HttpResponseBadRequest()

@login_required
def withdraw_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id, worker=request.user)
    if request.method == 'POST':
        application.delete()
        return JsonResponse({'status': 'success', 'message': 'Application withdrawn successfully.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)

@login_required
def update_application_status(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id, job__contractor=request.user)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['pending', 'accepted', 'rejected']:
            application.status = status
            application.save()
            
            Notification.objects.create(
                user=application.worker,
                message=f"Your application for {application.job.title} has been {status}."
            )
            
            return JsonResponse({'status': 'success', 'message': f'Application status updated to {status}.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid status.'}, status=400)
    return HttpResponseBadRequest()

@login_required
def edit_team_member(request, member_id):
    subworker = get_object_or_404(SubWorker, id=member_id, worker=request.user)
    if request.method == 'POST':
        form = SubWorkerForm(request.POST, instance=subworker)
        if form.is_valid():
            form.save()
            messages.success(request,'Team member updated successfully.')
            return redirect(reverse('accounts:worker_profile'))
        else:
            messages.success(request,'Error updating team member.')
            return redirect(reverse('accounts:worker_profile'))
    elif request.method == 'GET':
        data = {
            'id': subworker.id,
            'full_name': subworker.full_name,
            'contact_number': subworker.contact_number,
            'age': subworker.age,
            'gender': subworker.gender,
            'skills': subworker.skills
        }
        return JsonResponse(data)
    return HttpResponseBadRequest()

@login_required
def delete_team_member(request, member_id):
    subworker = get_object_or_404(SubWorker, id=member_id, worker=request.user)
    if request.method == 'POST':
        subworker.delete()
        return JsonResponse({'status': 'success', 'message': 'Team member deleted successfully.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)

@login_required
def update_profile_image(request):
    if request.method == 'POST' and request.FILES.get('profile_image'):
        profile = request.user.contractorprofile if request.user.user_type == 'contractor' else request.user.workerprofile
        profile.profile_image.delete(save=False)  # Remove old image
        profile.profile_image = request.FILES['profile_image']
        profile.save()
        return JsonResponse({'status': 'success', 'message': 'Profile image updated successfully.', 'image_url': profile.profile_image.url})
    return JsonResponse({'status': 'error', 'message': 'No image provided or invalid request.'}, status=400)

@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    notifications.filter(is_read=False).update(is_read=True)
    data = [{'message': n.message, 'created_at': n.created_at.isoformat(), 'is_read': n.is_read} for n in notifications]
    return JsonResponse({'notifications': data})

@login_required
def worker_detail(request, worker_id):
    worker = get_object_or_404(WorkerProfile, id=worker_id)
    average_rating = Rating.objects.filter(target_user=worker.user, rating_type='contractor_to_worker').aggregate(models.Avg('rating_value'))['rating_value__avg'] or 0
    language = request.session.get('language', 'en')
    return render(request, 'accounts/worker_detail.html', {'worker': worker, 'average_rating': average_rating, 'language': language})

@login_required
def rate_contractor(request, contractor_id):
    contractor = get_object_or_404(User, id=contractor_id, user_type='contractor')
    if request.user.user_type != 'worker':
        messages.error(request, 'Only workers can rate contractors.')
        return redirect('accounts:worker_dashboard')
    
    if not JobApplication.objects.filter(worker=request.user, job__contractor=contractor, status='accepted').exists():
        messages.error(request, 'You can only rate contractors for jobs you were accepted for.')
        return redirect('accounts:worker_dashboard')
    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.reviewer = request.user
            rating.target_user = contractor
            rating.rating_type = 'worker_to_contractor'
            rating.save()
            messages.success(request, 'Rating submitted successfully.')
            return redirect('accounts:worker_dashboard')
        else:
            messages.error(request, 'Error submitting rating.')
    else:
        form = RatingForm()
    language = request.session.get('language', 'en')
    return render(request, 'accounts/rate_contractor.html', {'form': form, 'contractor': contractor, 'language': language})

@login_required
def rate_worker(request, worker_id):
    worker = get_object_or_404(User, id=worker_id, user_type='worker')
    if request.user.user_type != 'contractor':
        messages.error(request, 'Only contractors can rate workers.')
        return redirect('accounts:contractor_dashboard')
    
    if not JobApplication.objects.filter(worker=worker, job__contractor=request.user, status='accepted').exists():
        messages.error(request, 'You can only rate workers for jobs you posted and accepted.')
        return redirect('accounts:contractor_dashboard')
    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.reviewer = request.user
            rating.target_user = worker
            rating.rating_type = 'contractor_to_worker'
            rating.save()
            messages.success(request, 'Rating submitted successfully.')
            return redirect('accounts:contractor_dashboard')
        else:
            messages.error(request, 'Error submitting rating.')
    else:
        form = RatingForm()
    language = request.session.get('language', 'en')
    return render(request, 'accounts/rate_worker.html', {'form': form, 'worker': worker, 'language': language})

@login_required
def rate_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    if request.user.user_type != 'worker':
        messages.error(request, 'Only workers can rate jobs.')
        return redirect('accounts:worker_dashboard')
    
    if not JobApplication.objects.filter(worker=request.user, job=job, status='accepted').exists():
        messages.error(request, 'You can only rate jobs you were accepted for.')
        return redirect('accounts:worker_dashboard')
    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.reviewer = request.user
            rating.target_job = job
            rating.rating_type = 'worker_to_job'
            rating.save()
            messages.success(request, 'Rating submitted successfully.')
            return redirect('accounts:worker_dashboard')
        else:
            messages.error(request, 'Error submitting rating.')
    else:
        form = RatingForm()
    language = request.session.get('language', 'en')
    return render(request, 'accounts/rate_job.html', {'form': form, 'job': job, 'language': language})

def about_us(request):
    language = request.session.get('language', 'en')
    return render(request, 'about_us.html', {'language': language})

def services(request):
    language = request.session.get('language', 'en')
    return render(request, 'services.html', {'language': language})

def help_center(request):
    language = request.session.get('language', 'en')
    return render(request, 'help_center.html', {'language': language})

@login_required
def accept_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id, job__contractor=request.user)
    if request.method == 'POST':
        application.status = 'accepted'
        application.save()
        messages.success(request, 'Application accepted successfully.')
        return JsonResponse({'status': 'success', 'message': 'Application accepted successfully.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)

@login_required
def reject_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id, job__contractor=request.user)
    if request.method == 'POST':
        application.status = 'rejected'
        application.save()
        messages.success(request, 'Application rejected successfully.')
        return JsonResponse({'status': 'success', 'message': 'Application rejected successfully.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)
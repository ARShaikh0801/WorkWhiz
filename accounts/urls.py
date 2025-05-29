from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('', views.index, name='index'),
    path('signup/', views.sign_up, name='sign_up'),
    path('login/', views.log_in, name='log_in'),
    path('logout/', views.log_out, name='log_out'),
    
    # Password Reset
    path('password_reset/', views.forget_password, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url='/reset/done/'
    ), name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
    
    # Contractor Views
    path('contractor_dashboard/', views.contractor_dashboard, name='contractor_dashboard'),
    path('contractor_profile/', views.contractor_profile, name='contractor_profile'),
    path('edit_contractor_profile/', views.edit_profile, name='edit_contractor_profile'),
    path('post_job/', views.post_job, name='post_job'),
    path('my_jobs/', views.my_jobs, name='my_jobs'),
    path('edit_job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),
    
    # Worker Views
    path('worker_dashboard/', views.worker_dashboard, name='worker_dashboard'),
    path('worker_profile/', views.worker_profile, name='worker_profile'),
    path('edit_worker_profile/', views.edit_profile, name='edit_worker_profile'),
    path('edit_team_member/<int:member_id>/', views.edit_team_member, name='edit_team_member'),
    path('delete_team_member/<int:member_id>/', views.delete_team_member, name='delete_team_member'),
    path('worker_detail/<int:worker_id>/', views.worker_detail, name='worker_detail'),
    
    # Job and Application Views
    path('get_job_details/<int:job_id>/', views.get_job_details, name='get_job_details'),
    path('submit_application/<int:job_id>/', views.submit_application, name='submit_application'),
    path('withdraw_application/<int:application_id>/', views.withdraw_application, name='withdraw_application'),
    path('update_application_status/<int:application_id>/', views.update_application_status, name='update_application_status'),
    path('accept_application/<int:application_id>/', views.accept_application, name='accept_application'),
    path('reject_application/<int:application_id>/', views.reject_application, name='reject_application'),
    
    # Profile Image Update
    path('update_profile_image/', views.update_profile_image, name='update_profile_image'),
    
    # Notifications
    path('notifications/', views.get_notifications, name='notifications'),
    
    # Rating Views
    path('rate_contractor/<int:contractor_id>/', views.rate_contractor, name='rate_contractor'),
    path('rate_worker/<int:worker_id>/', views.rate_worker, name='rate_worker'),
    path('rate_job/<int:job_id>/', views.rate_job, name='rate_job'),
    
    # Other Pages
    path('about_us/', views.about_us, name='about_us'),
    path('services/', views.services, name='services'),
    path('help_center/', views.help_center, name='help_center'),
]
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.Userlogin,name="user_login"),
    path('signup/',views.UserSignUp,name="user_signup"),
    path('dashboard/',views.UserDashboard,name="dashboard"),
    path('logout/',views.UserLogout,name='user_logout'),
    path('task/add',views.add_task,name='add_task'),
    path('task/update/<int:pk>/',views.update_task,name='update_task'),
    path('task/delete/<int:pk>/',views.delete_task,name='delete_task'),
    path('task/mark_done/<int:pk>/',views.mark_done,name='mark_done'),
    path('task/task_history',views.task_history,name='task_history'),
    path('task/details/<int:pk>/',views.task_details_view,name='task_details'),
    path('user/profile/',views.user_profile_view,name='user_profile_view'),
    path('task/upcoming/',views.upcoming_task_view,name="upcoming_task"),
    path('task/regular/',views.regular_tasks_view,name="regular_tasks"),
    path('singup/send_otp_mail/',views.send_mail_otp_view,name="send_mail_otp"),
    path('singup/validate_otp_mail/',views.validate_mail_otp_view,name="validate_mail_otp"),
    # path('user/profile/password_change',views.password_change_view,name='password_change_view'),
    
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='auth/password_reset.html'
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='auth/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='auth/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='auth/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    path(
    "password/change/",
    auth_views.PasswordChangeView.as_view(template_name="password_change.html"),
    name="password_change",
    ),
    path(
        "password/change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="password_changed_done.html"
        ),
        name="password_change_done"
    ),
    

    
]

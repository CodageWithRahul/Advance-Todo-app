from django.shortcuts import render, redirect
from .forms import SignUpForm, loginForm, TaskForm
from .models import Task, TaskInstance, UserDailyState, EmailOtp
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth import authenticate
from datetime import date, timedelta, datetime
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash
from .todoUtils import upcoming_tasks, email_otp_gen, email_otp_deleter, is_conflicting
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import smtplib
from django.db import transaction


def UserSignUp(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        SForm = SignUpForm(request.POST)
        if SForm.is_valid():
            email = SForm.cleaned_data.get("email").lower()
            try:
                email_otp = EmailOtp.objects.get(email=email)
            except EmailOtp.DoesNotExist:
                messages.error(request, "Please verify your email first")
                return redirect("user_signup")

            if not email_otp.is_verified:
                messages.error(request, "Email is not verified")
                return redirect("user_signup")

            user = SForm.save(commit=False)
            user.username = email
            user.save()
            email_otp.delete()
            login(request, user)
            messages.success(request, "Account is created")
            return redirect("dashboard")
        else:
            messages.error(request, "Correct a error Below!")
    else:
        SForm = SignUpForm()
    return render(request, "signup.html", {"SForm": SForm})


def Userlogin(request):

    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        LForm = loginForm(request.POST)
        if LForm.is_valid():
            email = LForm.cleaned_data.get("email")
            password = LForm.cleaned_data.get("password")
            remember_me = request.POST.get("remember_me")

            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                if remember_me:
                    # Session lasts 14 days
                    request.session.set_expiry(60 * 60 * 24 * 14)
                else:
                    # Session expires when browser closes
                    request.session.set_expiry(0)
                return redirect("dashboard")
            else:
                messages.error(request, "Credentials Invalid! | Try Again")
    else:
        LForm = loginForm()

    return render(request, "login.html", {"LForm": LForm})


@login_required(login_url="user_login")
def UserDashboard(request):
    loader(request)
    tasks = (
        TaskInstance.objects.filter(user=request.user, date=date.today())
        .exclude(Q(status=TaskInstance.FORWARDED) | Q(is_deleted=True))
        .select_related("task")
        .order_by("-status")
    )
    upcomingTask = upcoming_tasks(request.user, Task, Task.FUTURE, 7)
    for task in tasks:
        task.is_created_today = task.task.created_at.date() == date.today()
    return render(
        request,
        "dashboard.html",
        {"tasks": tasks, "todayDate": date.today(), "upcomingTask": upcomingTask},
    )


@login_required(login_url="user_login")
def UserLogout(request):
    logout(request)
    return redirect("user_login")


@login_required(login_url="user_login")
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task_type = form.cleaned_data.get("task_type", "").lower()
            start_date = form.cleaned_data.get("start_date")
            start_time = form.cleaned_data.get("startTime")
            end_time = form.cleaned_data.get("endTime")

            today_tasks = TaskInstance.objects.filter(
                user=request.user, date=date.today()
            ).exclude(Q(status=TaskInstance.FORWARDED) | Q(is_deleted=True))

            # 🔐 Time conflict check
            if start_time:
                # if (
                #     start_time < datetime.now().time().replace(microsecond=0)
                #     and task_type != "future"
                # ):
                #     messages.error(
                #         request,
                #         "You cannot create a task for a time that has already passed.",
                #     )
                #     return redirect("add_task")
                conflictTask = is_conflicting(today_tasks, start_time, end_time)
                if conflictTask != None:
                    print(conflictTask.task.title)
                    messages.error(
                        request,
                        f"Your time is conflicting with Task : {conflictTask.task.title}",
                    )
                    return redirect("add_task")

            # 📅 Future task validation
            if task_type == "future" and start_date <= date.today():
                messages.error(request, "Date must be greater than today")
                return redirect("add_task")

            task_obj = form.save(commit=False)
            task_obj.user = request.user
            task_obj.save()

            create_task_instance(task_obj)

            return redirect("dashboard")

        messages.error(request, "Something went wrong! | Task not added")

    else:
        form = TaskForm()

    return render(request, "task.html", {"task": form})


def create_task_instance(task):
    """
    Create TaskInstance ONLY if task is for today
    Future tasks will be handled later by scheduler/login logic test
    """
    if task.start_date is None or task.start_date == date.today():
        TaskInstance.objects.create(
            task=task,
            startTime=task.startTime,
            endTime=task.endTime,
            user=task.user,
            date=date.today(),
            status=TaskInstance.PENDING,
        )


@login_required(login_url="user_login")
def update_task(request, pk):
    try:
        getTask = get_object_or_404(Task, id=pk, user=request.user)
    except Task.DoesNotExist:
        messages.error(request, "Task not found")
        return redirect("dashboard")
    if request.method == "POST":
        task = TaskForm(request.POST, instance=getTask)
        if task.is_valid():

            task.save()
            return redirect("dashboard")
        else:
            messages.error(request, "Somthing is wrong! | Task not added")
            return redirect("dashboard")

    else:
        task = TaskForm(instance=getTask)
    return render(request, "task.html", {"task": task})


@login_required(login_url="user_login")
def delete_task(request, pk):
    try:
        getTask = TaskInstance.objects.get(id=pk, user=request.user)
    except TaskInstance.DoesNotExist:
        messages.error(request, "Task not found")
        return redirect("dashboard")

    if request.method == "POST":
        if getTask.task.created_at.date() == date.today():
            getTask.delete()
            getTask.task.delete()
            return redirect("dashboard")
        getTask.is_deleted = True
        getTask.deleted_at = timezone.now()

        task = getTask.task
        task.is_deleted = True
        task.is_active = False

        task.save()
        getTask.save()
        return redirect("dashboard")

    return render(request, "deletetask.html", {"task": getTask})


@login_required(login_url="user_login")
def mark_done(request, pk):
    task = get_object_or_404(TaskInstance, id=pk, user=request.user)
    if task.status == "DONE":
        task.status = "PENDING"
        task.task.is_active = True
        # messages.error(request,"Mark as Pending")
    else:
        task.status = "DONE"
        task.task.is_active = False
        # messages.success(request,"Mark As Done")

    task.task.save()
    task.save()

    return redirect("dashboard")


@login_required(login_url="user_login")
def task_details_view(request, pk):
    task = get_object_or_404(
        TaskInstance.objects.select_related("task"), id=pk, user=request.user
    )
    if request.method == "POST":
        remark = request.POST.get("remarks")
        task.remarks = remark
        task.save()

    source = request.GET.get("from")

    return render(request, "task_details.html", {"task": task, "source": source})


def loader(request):
    today = date.today()
    yesterday = today - timedelta(days=1)

    state, created = UserDailyState.objects.get_or_create(
        user=request.user, defaults={"last_updated": today}
    )

    # If already updated today → do nothing
    if state.last_updated == today:
        return

    pending_tasks = (
        TaskInstance.objects.filter(user=request.user, status="PENDING")
        .exclude(is_deleted=True)
        .select_related("task")
    )

    for task in pending_tasks:
        TaskInstance.objects.get_or_create(
            startTime=task.task.startTime,
            endTime=task.task.endTime,
            task=task.task,
            user=request.user,
            date=today,
            defaults={"status": "PENDING"},
        )
        task.status = "FORWARDED"
        task.save()

    tasks = Task.objects.filter(
        user=request.user,
        task_type="FUTURE",
        start_date__lte=date.today(),
        is_active=True,
    ).exclude(is_deleted=True)

    for Ftask in tasks:
        TaskInstance.objects.get_or_create(
            startTime=Ftask.startTime,
            endTime=Ftask.endTime,
            task=Ftask,
            user=request.user,
            date=date.today(),
            defaults={"status": "PENDING"},
        )

    regular_task = Task.objects.filter(
        user=request.user,
        task_type="REGULAR",
    ).exclude(is_deleted=True)

    for rTask in regular_task:
        TaskInstance.objects.get_or_create(
            startTime=rTask.startTime,
            endTime=rTask.endTime,
            task=rTask,
            user=request.user,
            date=today,
            defaults={"status": "PENDING"},
        )

    state.last_updated = today
    state.save()


@login_required(login_url="user_login")
def task_history(request):
    date = request.GET.get("date")
    tasks = (
        TaskInstance.objects.select_related("task").filter(date=date, user=request.user)
    ).order_by("-status")

    return render(request, "task_history.html", {"tasks": tasks, "selected_date": date})


@login_required(login_url="user_login")
def upcoming_task_view(request):
    upcomingTask = upcoming_tasks(request.user, Task, Task.FUTURE)
    return render(request, "upcoming_task.html", {"upTask": upcomingTask})


@login_required(login_url="user_login")
def regular_tasks_view(request):
    regularTask = Task.objects.filter(
        user=request.user,
        task_type=Task.REGULAR,
        is_deleted=False,
    )
    return render(request, "regular_task.html", {"reguTask": regularTask})


@login_required(login_url="user_login")
def user_profile_view(request):
    return render(request, "user_profile.html")


@require_POST
def send_mail_otp_view(request):
    print("EMAIL_HOST_USER:", settings.EMAIL_HOST_USER)
    print("EMAIL_HOST_PASSWORD exists:", bool(settings.EMAIL_HOST_PASSWORD))
    email = request.POST.get("email")
    fname = request.POST.get("first_name", "")
    lname = request.POST.get("last_name", "")

    if not email:
        return JsonResponse(
            {"success": False, "message": "Email is required"}, status=400
        )

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse(
            {"success": False, "message": "Invalid email address"}, status=400
        )

    full_name = f"{fname} {lname}".strip()
    otp = email_otp_gen()

    try:
        with transaction.atomic():
            EmailOtp.objects.update_or_create(
                email=email.lower(), defaults={"otp": otp, "is_verified": False}
            )

            sendMailOTP(email=email, name=full_name, otp=otp)

    except smtplib.SMTPException:
        return JsonResponse(
            {
                "success": False,
                "message": "Unable to send email. Please try again later",
            },
            status=500,
        )

    except Exception:
        return JsonResponse(
            {"success": False, "message": "Something went wrong"}, status=500
        )

    return JsonResponse(
        {"success": True, "message": "OTP sent successfully", "email": email}
    )


def sendMailOTP(email, name, otp):
    subject = f"Welcome {name} To our Platform"
    bodymess = render_to_string(
        "emailAuth/email_otp_sender.html", {"name": name, "otp": otp}
    )

    from_email = settings.EMAIL_HOST_USER
    recipient = [email]

    mail = EmailMessage(subject, bodymess, from_email, recipient)
    mail.content_subtype = "html"
    mail.send()
    # mail.send(fail_silently=False)


@require_POST
def validate_mail_otp_view(request):
    email = request.POST.get("email")
    user_otp = request.POST.get("otp")

    if not email or not user_otp:
        return JsonResponse(
            {"success": False, "message": "Email and OTP are required"}, status=400
        )

    email = email.lower()
    user_otp = user_otp.strip()

    otp_record = EmailOtp.objects.filter(email=email).first()

    if not otp_record:
        return JsonResponse(
            {"success": False, "message": "Email not found"}, status=404
        )

    if otp_record.is_expired():
        return JsonResponse({"success": False, "message": "OTP expired"}, status=400)

    if otp_record.otp != user_otp:
        return JsonResponse({"success": False, "message": "Invalid OTP"}, status=400)

    otp_record.is_verified = True
    otp_record.save(update_fields=["is_verified"])

    return JsonResponse({"success": True, "message": "Email verified successfully"})


# this is also can changed password but django have build in method and url to change password using old password we use them

# @login_required(login_url='user_login')
# def password_change_view(request):
#     user = request.user
#     if request.method == 'POST':
#         # user = User.objects.get(id=request.user.id)
#         oldPassword =  request.POST.get('oldPasssword')
#         newPassword1 =  request.POST.get('Npassword1')
#         newPassword2 =  request.POST.get('Npassword1')
#         print(oldPassword)
#         print(newPassword1)
#         print(newPassword2)

#         # Check old password
#         if not user.check_password(oldPassword):
#             messages.error(request, "Old password is incorrect")
#             return redirect('password_change')

#          # Check new passwords match
#         if newPassword1 != newPassword2:
#             messages.error(request, "New passwords do not match")
#             return redirect('password_change')

#         user.set_password(newPassword1)
#         user.save()

#          # IMPORTANT: keep user logged in
#         update_session_auth_hash(request, user)

#         return redirect('password_change_done')
#     return render(request,'password_change.html')

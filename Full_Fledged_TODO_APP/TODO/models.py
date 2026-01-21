# todos/models.py

from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta,datetime


class Task(models.Model):
    TODAY = "TODAY"
    FUTURE = "FUTURE"
    REGULAR = "REGULAR"

    TASK_TYPE_CHOICES = [
        (TODAY, "Today"),
        (FUTURE, "Future"),
        (REGULAR, "Regular"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    title = models.CharField(max_length=255)
    task_type = models.CharField(
        max_length=10,
        choices=TASK_TYPE_CHOICES,
        default=TODAY
    )
    start_date = models.DateField(
        null=True,
        blank=True,
        help_text="Used only for future tasks"
    )
    startTime = models.TimeField(blank=True,null=True)
    endTime = models.TimeField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class TaskInstance(models.Model):
    PENDING = "PENDING"
    DONE = "DONE"
    FORWARDED = "FORWARDED"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (DONE, "Done"),
        (FORWARDED, "Forwarded"),
    ]

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="instances"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="task_instances"
    )
    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    startTime = models.TimeField(blank=True,null=True)
    endTime = models.TimeField(blank=True,null=True)
    
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True,blank=True)
    remarks = models.TextField(blank=True,null=True,default=None)
    

    class Meta:
        unique_together = ("task", "date")

    def __str__(self):
        return f"{self.task.title} - {self.date}"


class UserDailyState(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="daily_state"
    )
    last_updated = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.last_updated}"
    
    
class EmailOtp(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)
    
    def __str__(self):
        return self.email

# todos/models.py

from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime


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
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks"
    )
    title = models.CharField(max_length=255)
    task_type = models.CharField(
        max_length=10, choices=TASK_TYPE_CHOICES, default=TODAY
    )
    start_date = models.DateField(
        null=True, blank=True, help_text="Used only for future tasks"
    )
    link = models.URLField(blank=True, null=True)

    startTime = models.TimeField(blank=True, null=True)
    endTime = models.TimeField(blank=True, null=True)
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

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="instances")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="task_instances",
    )
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True, null=True, default=None)

    class Meta:
        unique_together = ("task", "date")

    def __str__(self):
        return f"{self.task.title} - {self.date}"


class UserDailyState(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="daily_state"
    )
    last_updated = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.last_updated}"


class EmailOtp(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return self.email


class Goals(models.Model):

    URGENT = "URGENT"
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"

    PRIORITY_CHOICES = [
        (URGENT, "Urgent"),
        (HIGH, "High"),
        (MODERATE, "Moderate"),
        (LOW, "Low"),
    ]

    PRIORITY_ORDER_MAP = {
        URGENT: 1,
        HIGH: 2,
        MODERATE: 3,
        LOW: 4,
    }

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="goals"
    )

    goal_title = models.CharField(max_length=300)

    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=HIGH)

    priority_order = models.PositiveSmallIntegerField(default=2)

    deadline = models.DateField()
    isDone = models.BooleanField(default=False)
    isDelete = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["priority_order", "deadline"]

    def save(self, *args, **kwargs):
        self.priority_order = self.PRIORITY_ORDER_MAP.get(self.priority, 5)
        super().save(*args, **kwargs)


class CoinWallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(default=0)

    def apply_transaction(self, coins, source, taskInstance=None, goal=None):
        if self.balance + coins < 0:
            coins = -self.balance

        CoinTransaction.objects.create(
            user=self.user,
            source=source,
            taskInstance=taskInstance,
            goal=goal,
            coins=coins,
        )

        self.balance += coins
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.balance}"


class CoinTransaction(models.Model):

    REWARD_SOURCE = [
        ("task", "Task Completion"),
        ("goal", "Goal Completion"),
        ("login", "Daily Login"),
        ("streak", "Streak Bonus"),
        ("undo", "Undo Task"),
        ("notInTime", "Not done within the time"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    source = models.CharField(max_length=20, choices=REWARD_SOURCE)

    taskInstance = models.ForeignKey(
        TaskInstance, on_delete=models.CASCADE, null=True, blank=True
    )
    goal = models.ForeignKey(Goals, on_delete=models.CASCADE, null=True, blank=True)

    coins = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Notes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    note = models.TextField()
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

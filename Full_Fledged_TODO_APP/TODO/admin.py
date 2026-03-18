from django.contrib import admin
from .models import (
    Task,
    TaskInstance,
    UserDailyState,
    CoinWallet,
    CoinTransaction,
    Goals,
    Notes,
)

# Register your models here.
admin.site.register(Task)
admin.site.register(TaskInstance)
admin.site.register(UserDailyState)
admin.site.register(CoinWallet)
admin.site.register(CoinTransaction)
admin.site.register(Goals)
admin.site.register(Notes)

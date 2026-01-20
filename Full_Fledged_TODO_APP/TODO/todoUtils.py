from datetime import date,timedelta
import random

def upcoming_tasks(user,dbTable,task_type,days=None):
    upcomingTask = dbTable.objects.filter(
        user = user,
        task_type = task_type,
        start_date__gt = date.today()
    ).order_by('start_date')
    
    if days:
        upcomingTask = upcomingTask.filter(
            start_date__range = (date.today()+timedelta(days=1),date.today() + timedelta(days=days))
        )
    return upcomingTask



#email otp generator

def email_otp_gen():    
    return str(random.randint(100000, 999999))

def email_otp_deleter(dbTable,email):
    getMail = dbTable.objects.get(email=email)
    getMail.delete()
    
    
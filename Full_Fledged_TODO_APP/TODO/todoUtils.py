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
    
    
    
def is_conflicting(db_tasks, user_start, user_end):
    if not user_start:
        return False

    # Normalize user time
    user_end = user_end or user_start

    for task in db_tasks:
        db_start = task.startTime
        db_end = task.endTime or db_start

        # Defensive: skip invalid DB records
        if not db_start:
            continue

        # Universal overlap check
        if db_start <= user_end and user_start <= db_end:
            return True

    return False



from .models import Log

def create_log(user, action, details=None):
    Log.objects.create(
        user=user,
        action=action,
        details=details
    )
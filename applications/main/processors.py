from .models import Preference

def preference(*args, **kwargs):
    return {
        'preference': Preference.objects.first() or {}
    }

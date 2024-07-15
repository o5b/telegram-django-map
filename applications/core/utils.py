from django.contrib.admin.models import ADDITION, LogEntry
from django.contrib.admin.options import get_content_type_for_model


def logger(
    *,
    obj,
    user,
    message,
    action_flag=ADDITION,
):
    """Записать в LogEntry сообщение по объекту"""
    LogEntry.objects.log_action(
        user_id=user.pk,
        content_type_id=get_content_type_for_model(obj).pk,
        object_id=obj.pk,
        object_repr=str(obj),
        action_flag=action_flag,
        change_message=message,
    )

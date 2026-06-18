from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()


@shared_task
def send_confirmation_email(code, email):
    send_mail(
        "Подтверждение регистрации",
        f"Ваш код подтверждения: {code}",
        "noreply@shopapi.com",
        [email],
        fail_silently=False,
    )
    return "OK"


@shared_task
def delete_inactive_users():
    deleted_count, _ = User.objects.filter(is_active=False).delete()
    print(f"Deleted {deleted_count} inactive users")
    return "DELETED"

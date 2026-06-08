from datetime import date, datetime

from rest_framework.exceptions import ValidationError


def validate_user_is_adult(birthday):
    if not birthday:
        raise ValidationError("Дата рождения не указана.")

    if isinstance(birthday, str):
        try:
            birthday = datetime.fromisoformat(birthday).date()
        except ValueError:
            raise ValidationError("Неправильный формат даты рождения.")

    if not isinstance(birthday, date):
        raise ValidationError("Неправильный формат даты рождения.")

    today = date.today()
    age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

    if age < 18:
        raise ValidationError("Вам должно быть 18 лет, чтобы создать продукт.")

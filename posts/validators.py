import re
from datetime import date

from django.core.exceptions import ValidationError


def validate_password(password):
    """
    Валидация password:
    - пароль должен быть длиной не менее 8 символов
    - пароль должен содержать цифры).
    """
    if len(password) < 8:
        raise ValidationError("Пароль должен содержать минимум 8 символов.")
    if not re.search(r"\d", password):
        raise ValidationError("Пароль должен содержать цифры")
    return password


def validate_email(value):
    """
    Валидация email:
    - разрешены домены: mail.ru, yandex.ru
    """
    allowed_domains = ["mail.ru", "yandex.ru"]
    domain = value.split("@")[-1].lower()

    if domain not in allowed_domains:
        raise ValidationError(f"Разрешены только следующие домены: {', '.join(allowed_domains)}")

    return value


def validate_author_age(birth_date):
    """
    Валидация возраста (18+)
    """
    print(birth_date)
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if age < 18:
        raise ValidationError("Пользователь должен быть старше 18 лет")

    return birth_date


def validate_title(value):
    """
    Валидация на отсутствие запрещенных слов
    """
    forbidden_words = ["ерунда", "глупость", "чепуха", "бред"]
    lower_value = value.lower()
    for word in forbidden_words:
        if word in lower_value:
            raise ValidationError(f"Текст содержит запрещенное слово: '{word}'")

    return value

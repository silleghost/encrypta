# validators.py
from django.core.validators import RegexValidator

# Регулярное выражение для проверки наличия только букв латинского алфавита
latin_alphabet_regex = RegexValidator(
    r'^[a-zA-Z]*$',
    'Поле должно содержать только буквы латинского алфавита.'
)
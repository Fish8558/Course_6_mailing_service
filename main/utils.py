import secrets
import string
from django.forms import BooleanField


class StyleFormMixin:
    """Класс миксин стилизации формы"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fields_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = "form-check-input"
            else:
                field.widget.attrs['class'] = "form-control"


def make_random_password():
    character = string.ascii_letters + string.digits
    password = "".join(secrets.choice(character) for i in range(15))
    return password

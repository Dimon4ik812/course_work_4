from django import forms
from django.contrib.auth.forms import UserCreationForm
from newapp.models import StyleFormMixin

from .models import CustomsUser


class CustomUserCreationForm(StyleFormMixin, UserCreationForm):
    phone_number = forms.CharField(
        max_length=15, required=False, help_text="Необязательное поле. Введите номер телефона"
    )
    username = forms.CharField(max_length=50, required=True)

    class Meta:
        model = CustomsUser
        fields = ("email", "avatar", "first_name", "username", "phone_number", "country")
        exclude = (
            "is_blocked",
            "last_login",
            "is_superuser",
            "is_staff",
            "groups",
            "user_permissions",
            "date_joined",
            "is_active",
            "token",
        )  # Добавьте недостающие поля для исключения

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        first_name = cleaned_data.get("first_name")

        if (
            username
            and first_name
            and (
                username.lower()
                in ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]
                or first_name.lower()
                in ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]
            )
        ):
            self.add_error("username", "Запрещенное слово")
            self.add_error("first_name", "Запрещенное слово")
        return cleaned_data  # обязательно вернуть cleaned_data

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")

        if avatar is None:
            return None

        if avatar.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Размер файла не должен превышать 5MB.")

        if not avatar.name.endswith((".jpg", ".jpeg", ".png")):
            raise forms.ValidationError(
                "Формат файла не соответствует требованиям. Допустимые форматы: *.jpg, *.jpeg, *.png"
            )

        return avatar

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Номер телефона должен состоять только из цифр")
        return phone_number

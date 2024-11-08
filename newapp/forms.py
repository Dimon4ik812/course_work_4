from django import forms
from django.forms import BooleanField

from newapp.models import Message, Newsletter


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs["class"] = "form-check-input"
            else:
                fild.widget.attrs["class"] = "form-control"

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ("owner",)

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields["subject"].widget.attrs.update(
            {
                "class": "form-control",  # Добавление CSS-класса для стилизации поля
                "placeholder": "Введите название продукта",
            }
        )  # Текст подсказки внутри поля

        self.fields["body_of_the_letter"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите описание продукта"}
        )



class NewsletterForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Newsletter
        exclude = (
            "owner",
            "is_blocked",
            "success",
        )



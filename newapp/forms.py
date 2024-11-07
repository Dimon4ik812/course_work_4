from django import forms

from newapp.models import Message, Newsletter, StyleFormMixin


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

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("subject")
        description = cleaned_data.get("body_of_the_letter")

        if name.lower() and description.lower() in [
            "казино",
            "криптовалюта",
            "крипта",
            "биржа",
            "дешево",
            "бесплатно",
            "обман",
            "полиция",
            "радар",
        ]:
            self.add_error("name", "запрещенное слово")
            self.add_error("description", "запрещенное слово")


class NewsletterForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Newsletter
        exclude = (
            "owner",
            "is_blocked",
            "success",
        )

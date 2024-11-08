from django.contrib import admin

from .models import MailingAttempt, MailingRecipient, Message, Newsletter


@admin.register(MailingRecipient)
class MailingRecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name", "comment")
    list_filter = ("full_name",)
    search_fields = (
        "full_name",
        "email",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "body_of_the_letter")
    list_filter = ("subject",)
    search_fields = ("subject",)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "message")
    list_filter = ("status",)
    search_fields = ("status",)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "mail_server_response")
    list_filter = ("status",)
    search_fields = ("status",)

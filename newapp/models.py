import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import BooleanField


from users.models import CustomsUser

logger = logging.getLogger(__name__)


class MailingRecipient(models.Model):
    """Модель «Получатель рассылки»:"""

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, verbose_name="Ф.И.О")
    comment = models.TextField()
    owner = models.ForeignKey(CustomsUser, verbose_name="Владелец", blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["full_name", "email"]
        permissions = [
            ("can_view_all_mailingrecipient", "can view all mailingrecipient"),
        ]


class Message(models.Model):
    """Модель «Сообщение»:"""

    subject = models.CharField(max_length=250, verbose_name="тема письма")
    body_of_the_letter = models.TextField(verbose_name="Сообщение")
    owner = models.ForeignKey(CustomsUser, verbose_name="Владелец", blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщений"
        ordering = ["subject"]
        permissions = [
            ("can_view_all_messages", "can view all messages"),
        ]


class Newsletter(models.Model):
    """Модель «Рассылка»:"""

    STATUS_CHOICES = [("завершена", "завершена"), ("создана", "создана"), ("запущена", "запущена")]

    sent_date = models.DateTimeField(auto_now_add=True)
    end_of_sending = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="создана")
    message = models.OneToOneField(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(MailingRecipient, verbose_name="Получатели")
    owner = models.ForeignKey(CustomsUser, verbose_name="Владелец", blank=True, null=True, on_delete=models.SET_NULL)
    is_blocked = models.BooleanField(default=False)
    success = models.BooleanField(default=False)

    def __str__(self):
        return f"Рассылка с {self.recipients.count()} получателями"

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ["status", "sent_date", "end_of_sending"]
        permissions = [
            ("can_view_all_mailings", "can view all mailings"),
            ("can_disable_mailings", "can disable mailings"),
        ]

    def block_mailing(self):
        self.is_blocked = True
        self.save()
        logging.info(f"Рассылка {self.pk} заблокирована пользователем {self.owner}")

    def unblock_mailing(self):
        self.is_blocked = False
        self.save()
        logging.info(f"Рассылка {self.pk} разблокирована пользователем {self.owner}")


class MailingAttempt(models.Model):
    """Модель «Попытка рассылки»"""

    STATUS_CHOICES = [("успешно", "успешно"), ("не успешно", "не успешно")]

    Date_and_time_of_attempt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    Mail_server_response = models.TextField(blank=True)  # Разрешаем пустое значение
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, related_name="attempts")
    recipients = models.ManyToManyField(MailingRecipient, blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"
        ordering = ["status", "Date_and_time_of_attempt"]
        permissions = [
            ("can_view_all_mailings_attempts", "can view all mailings attempts"),
        ]


class UserMailingStatistics(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # Используем settings.AUTH_USER_MODEL
    total_mailings = models.IntegerField(default=0)
    successful_mailings = models.IntegerField(default=0)
    failed_mailings = models.IntegerField(default=0)

    def update_statistics(self):
        self.total_mailings = Newsletter.objects.filter(owner=self.user).count()
        self.successful_mailings = Newsletter.objects.filter(owner=self.user, status="success").count()
        self.failed_mailings = Newsletter.objects.filter(
            owner=self.user, status__in=["failed", "partially_success"]
        ).count()
        self.save()  # Удаляем save() из update_statistics

    def __str__(self):
        return f"Statistics for {self.user.username}"



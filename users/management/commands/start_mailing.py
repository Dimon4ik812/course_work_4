from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from newapp.models import MailingAttempt, Newsletter


class Command(BaseCommand):
    help = "Запускает рассылку по указанному ID."

    def add_arguments(self, parser):
        parser.add_argument("newsletter_id", type=int, help="ID рассылки")

    @transaction.atomic
    def handle(self, *args, **options):
        newsletter_id = options["newsletter_id"]
        try:
            newsletter = Newsletter.objects.get(pk=newsletter_id)
        except Newsletter.DoesNotExist:
            raise CommandError(f"Рассылка с ID {newsletter_id} не найдена.")

        recipients = newsletter.recipients.all()
        if not recipients:
            raise CommandError(f"У рассылки с ID {newsletter_id} нет получателей.")

        # Создание попытки рассылки
        attempt = MailingAttempt(newsletter=newsletter, owner=newsletter.owner)  # Используем owner из Newsletter
        attempt.save()

        successful_recipients = []
        responses = []

        for recipient in recipients:
            try:
                send_mail(
                    newsletter.message.subject,
                    newsletter.message.body_of_the_letter,
                    settings.EMAIL_HOST_USER,  # Используем настройку из settings.py
                    [recipient.email],
                    fail_silently=False,
                )
                successful_recipients.append(recipient)
                responses.append(f"Успешно: {recipient.email}")
            except Exception as e:
                responses.append(f"Неуспешно: {recipient.email} - {str(e)}")

        attempt.recipients.set(successful_recipients)
        attempt.Mail_server_response = "\n".join(responses)

        # Обновление статуса Newsletter
        if len(successful_recipients) == len(recipients):
            newsletter.status = "success"
        elif len(successful_recipients) > 0:
            newsletter.status = "partially_success"
        else:
            newsletter.status = "failed"
        newsletter.save()

        attempt.status = newsletter.status
        attempt.save()

        successful_count = len(successful_recipients)
        failed_count = len(recipients) - successful_count

        self.stdout.write(
            self.style.SUCCESS(
                f"Рассылка {newsletter_id} завершена! Успешно: {successful_count}, Неуспешно: {failed_count}\nОтчеты:\n{attempt.Mail_server_response}"
            )
        )

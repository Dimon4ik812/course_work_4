from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DeleteView, DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from config.settings import EMAIL_HOST_USER
from newapp.forms import MessageForm, NewsletterForm
from newapp.models import MailingAttempt, MailingRecipient, Message, Newsletter, UserMailingStatistics
from newapp.services import get_recipient_from_cache


class MailingRecipientListView(ListView):
    model = MailingRecipient
    template_name = "newapp/mailing_list.html"
    context_object_name = "newapps"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return get_recipient_from_cache()
        else:
            user = self.request.user
            return MailingRecipient.objects.filter(owner=user)


class MailingRecipientCreateView(CreateView):
    model = MailingRecipient
    fields = ["email", "full_name", "comment"]
    template_name = "newapp/mailing_create.html"
    success_url = reverse_lazy("newapp:mailingrecipient_list")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user  # Устанавливаем владельца из текущего пользователя
        instance.save()
        return super().form_valid(form)


class MailingRecipientView(DetailView):
    model = MailingRecipient
    template_name = "newapp/mailingrecipient_detail.html"
    context_object_name = "newapp"


class MailingRecipientUpdateView(UpdateView):
    model = MailingRecipient
    fields = ["email", "full_name", "comment"]
    template_name = "newapp/mailing_create.html"
    success_url = reverse_lazy("newapp:mailingrecipient_list")


class MailingRecipientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MailingRecipient
    template_name = "newapp/mailing_delete.html"
    success_url = reverse_lazy("newapp:mailingrecipient_list")

    def test_func(self):
        mailing_recipient = self.get_object()  # Получаем объект MailingRecipient
        return self.request.user.is_authenticated and (
            self.request.user.has_perm("spam.delete_mailingrecipient") or self.request.user == mailing_recipient.owner
        )

    def handle_no_permission(self):
        return redirect("newapp:mailingrecipient_list")


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = "newapp/message_create.html"
    success_url = reverse_lazy("newapp:message_list")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user  # Устанавливаем владельца из request.user
        instance.save()
        return super().form_valid(form)


class MessageListView(ListView):
    model = Message
    template_name = "newapp/message_list.html"
    context_object_name = "newapps"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return get_recipient_from_cache()
        else:
            user = self.request.user
            return Message.objects.filter(owner=user)


class MessageView(DetailView):
    model = Message
    template_name = "newapp/message_detail.html"
    context_object_name = "newapp"


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "newapp/message_create.html"
    success_url = reverse_lazy("newapp:home")


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    template_name = "newapp/message_delete.html"
    success_url = reverse_lazy("newapp:message_list")

    def test_func(self):
        message = self.get_object()
        return self.request.user.is_authenticated and (
            self.request.user == message.owner or self.request.user.has_perm("newapp.delete_message")
        )

    def handle_no_permission(self):
        return redirect("newapp:message_list")


class NewsletterCreateView(CreateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = "newapp/newsletter_create.html"
    success_url = reverse_lazy("newapp:newsletter_list")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user  # Устанавливаем владельца из request.user
        instance.save()
        return super().form_valid(form)


class NewsletterListView(ListView):
    model = Newsletter
    template_name = "newapp/Newsletter_list.html"
    context_object_name = "newapps"


class NewsletterView(DetailView):
    model = Newsletter
    template_name = "newapp/newsletter_detail.html"
    context_object_name = "newapp"

    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.is_staff or self.request.user.has_perm("newapp.view_newsletter")
        )

    def handle_no_permission(self):
        return HttpResponseForbidden("У Вас нет прав для просмотра списка рассылок.")


class NewsletterUpdateView(UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = "newapp/newsletter_create.html"
    success_url = reverse_lazy("newapp:newsletter_list")

    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.is_staff or self.request.user.has_perm("newapp.newsletter_update")
        )

    def handle_no_permission(self):
        return HttpResponseForbidden("У Вас нет прав для просмотра списка рассылок.")


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingRecipient
    template_name = "newapp/newsletter_delete.html"
    success_url = reverse_lazy("newapp:home")

    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.is_staff or self.request.user.has_perm("newapp.newsletter_delete")
        )

    def handle_no_permission(self):
        return HttpResponseForbidden("У Вас нет прав для просмотра списка рассылок.")


class HomeView(TemplateView):
    template_name = "newapp/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_campaigns"] = Newsletter.objects.count()
        context["active_campaigns"] = Newsletter.objects.filter(status="started").count()
        context["unique_recipients"] = MailingRecipient.objects.count()
        return context


class MailingAttemptListView(ListView):
    model = MailingAttempt
    template_name = "newapp/mailing_attempt_list.html"
    context_object_name = "newapps"


@method_decorator(login_required, name="dispatch")
class SendNewsletterView(View):
    def post(self, request, pk):
        newsletter = get_object_or_404(Newsletter, pk=pk)
        recipients = newsletter.recipients.all()

        # Создание попытки рассылки и СОХРАНЕНИЕ
        attempt = MailingAttempt(newsletter=newsletter, owner=request.user)
        attempt.save()

        successful_recipients = []
        responses = []

        for recipient in recipients:
            try:
                send_mail(
                    newsletter.message.subject,
                    newsletter.message.body_of_the_letter,
                    EMAIL_HOST_USER,
                    [recipient.email],
                    fail_silently=False,
                )
                successful_recipients.append(recipient)
                responses.append(f"Успешно: {recipient.email}")
            except Exception as e:
                responses.append(f"Неуспешно: {recipient.email} - {str(e)}")

        attempt.recipients.set(successful_recipients)  # Теперь это работает корректно
        attempt.Mail_server_response = "\n".join(responses)

        # Обновление статуса Newsletter
        newsletter.status = "завершена"  # Статус всегда "Завершена"
        newsletter.success = len(successful_recipients) == len(recipients)  # Успешность рассылки
        newsletter.save()

        attempt.status = newsletter.status
        attempt.save()

        successful_count = len(successful_recipients)
        failed_count = len(recipients) - successful_count

        return HttpResponse(
            f"Рассылка завершена! Успешно: {successful_count}, Неуспешно: {failed_count}\nОтчеты:\n{attempt.Mail_server_response}"
        )


class BlockMailingView(LoginRequiredMixin, View):

    def get(self, request, mailing_id):
        mailing = get_object_or_404(Newsletter, id=mailing_id)
        return render(request, "newapp/newsletter_block.html", {"mailing": mailing})

    def post(self, request, mailing_id):
        mailing = get_object_or_404(Newsletter, id=mailing_id)

        if not request.user.has_perm("spam.can_disable_mailings"):
            return HttpResponseForbidden("У вас нет прав для блокировки рассылки.")

        is_blocked = request.POST.get("is_blocked")
        mailing.is_blocked = is_blocked == "on"
        mailing.save()
        return redirect("newapp:newsletter_list")


class UserMailingStatisticsView(View):
    def get(self, request):
        user_stats, created = UserMailingStatistics.objects.get_or_create(user=request.user)

        # Обновляем статистику
        user_stats.total_mailings = Newsletter.objects.filter(owner=request.user).count()
        user_stats.successful_mailings = Newsletter.objects.filter(owner=request.user, success=True).count()
        user_stats.failed_mailings = Newsletter.objects.filter(owner=request.user, success=False).count()
        user_stats.save()  # Сохраняем изменения в объект UserMailingStatistics

        return render(request, "newapp/user_statistics.html", {"user_stats": user_stats})


class MailingClearAttemptsView(View):

    def post(self, request):
        MailingAttempt.objects.all().delete()
        return redirect("newapp:mailing_attempt_list")

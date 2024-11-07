from django.urls import path

from newapp.apps import NewappConfig
from newapp.views import (
    BlockMailingView,
    HomeView,
    MailingAttemptListView,
    MailingClearAttemptsView,
    MailingRecipientCreateView,
    MailingRecipientDeleteView,
    MailingRecipientListView,
    MailingRecipientUpdateView,
    MailingRecipientView,
    MessageCreateView,
    MessageDeleteView,
    MessageListView,
    MessageUpdateView,
    MessageView,
    NewsletterCreateView,
    NewsletterDeleteView,
    NewsletterListView,
    NewsletterUpdateView,
    NewsletterView,
    SendNewsletterView,
    UserMailingStatisticsView,
)

app_name = NewappConfig.name

urlpatterns = [
    path("message_list/", MessageListView.as_view(), name="message_list"),
    path("message_detail/<int:pk>/", MessageView.as_view(), name="message_detail"),
    path("message_create/", MessageCreateView.as_view(), name="message_create"),
    path("message_update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"),
    path("message_delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"),
    path("mailingrecipient_detail/<int:pk>/", MailingRecipientView.as_view(), name="MailingRecipient_detail"),
    path("mailing_list/", MailingRecipientListView.as_view(), name="mailingrecipient_list"),
    path("mailing_create/", MailingRecipientCreateView.as_view(), name="MailingRecipient_create"),
    path("home/<int:pk>/update/", MailingRecipientUpdateView.as_view(), name="MailingRecipient_update"),
    path("home/<int:pk>/delete/", MailingRecipientDeleteView.as_view(), name="MailingRecipient_delete"),
    path("newsletter_list/", NewsletterListView.as_view(), name="newsletter_list"),
    path("newsletter_detail/<int:pk>/", NewsletterView.as_view(), name="newsletter_detail"),
    path("newsletter_create", NewsletterCreateView.as_view(), name="newsletter_create"),
    path("newsletter_update/<int:pk>/", NewsletterUpdateView.as_view(), name="newsletter_update"),
    path("newsletter_delete/<int:pk>/", NewsletterDeleteView.as_view(), name="newsletter_delete"),
    path("home/", HomeView.as_view(), name="home"),
    path("message_attempt_list/", MailingAttemptListView.as_view(), name="message_attempt_list"),
    path("send_newsletter/<int:pk>/", SendNewsletterView.as_view(), name="send_newsletter"),
    path(
        "newsletter_block/<int:mailing_id>/block/",
        BlockMailingView.as_view(),
        name="newsletter_block",
    ),
    path("user/statistics/", UserMailingStatisticsView.as_view(), name="user_statistics"),
    path(
        "clear-mailing-attempts/",
        MailingClearAttemptsView.as_view(),
        name="clear_mailing_attempts",
    ),
]

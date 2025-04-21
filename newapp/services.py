from django.core.cache import cache

from config.settings import CACHE_ENABLED
from newapp.models import MailingRecipient, Message, Newsletter


def get_message_from_cache():
    """Получает данные из кэша, если кэш пуст, получает данные из бд"""
    if not CACHE_ENABLED:
        return Message.objects.all()
    key = "message_list"
    message = cache.get(key)
    if message is not None:
        return message
    products = Message.objects.all()
    cache.set(key, products)
    return message


def get_recipient_from_cache():
    """Получает данные из кэша, если кэш пуст, получает данные из бд"""
    if not CACHE_ENABLED:
        return MailingRecipient.objects.all()
    key = "mailingrecipient_list"
    recipient = cache.get(key)
    if recipient is not None:
        return recipient
    products = MailingRecipient.objects.all()
    cache.set(key, products)
    return recipient


def get_newsletter_from_cache():
    """Получает данные из кэша, если кэш пуст, получает данные из бд"""
    if not CACHE_ENABLED:
        return Newsletter.objects.all()
    key = "newsletter_list"
    newletter = cache.get(key)
    if newletter is not None:
        return newletter
    products = Newsletter.objects.all()
    cache.set(key, products)
    return newletter

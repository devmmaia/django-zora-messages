import logging
import inspect
from django_zora_messages.models import Message, MessageLocation
from functools import lru_cache
from django.conf import settings
from django.utils import translation

logger = logging.getLogger(__name__)


def get_value(key, *args, **kwargs):
    return get_message(key, *args, **kwargs).value


def get_message(key, *args, **kwargs):
    # get language from arg or use the current language in use
    language_ = kwargs.get("language_", translation.get_language())

    if settings.DEBUG:
        return __get_or_create_message(key, *args, **kwargs)
    else:
        message = __get_or_empty_message(key, language_)
    return __format_message(message, *args, **kwargs)


def cache_clear():
    """ clear the cached messages """
    __get_or_empty_message.cache_clear()


@lru_cache(maxsize=3000)
def __get_or_empty_message(key, language_):
    try:
        # this is the ideal behavior
        message = Message.objects.get(key=key, language=language_)
    except Message.DoesNotExist:
        logger.error(f"zora_messages: key %s not found for language %s",
                     key, language_)
        # looks for a similar language in database
        # example: when pt-br is not found, looks for pt
        if '-' in language_:
            try:
                lang2 = language_[0:language_.find('-')]
                message = Message.objects.get(key=key, language=lang2)
                logger.warning(
                    f"using language %s instead of %s for key %s ",
                    lang2, language_, key)
            except Message.DoesNotExist:
                message = __empty_message(key, language_)
        else:
            message = __empty_message(key, language_)
    return message


def __empty_message(key, language_):
    """ used in production to avoid the system to be aborted """
    return Message(key=key, value=key, language=language_,
                   detailed=key)


def __get_or_create_message(key, *args, **kwargs):
    """ used in development to create a new message """
    language_ = kwargs.get("language_", translation.get_language())
    message, new_ = Message.objects.get_or_create(key=key, language=language_)

    if new_:
        logger.info(f"zora_messages:Created a new message for key: {key}")
        message.value = key
        message.save()
    location = _get_location()

    if location not in message.locations:
        MessageLocation.objects.create(key=key, location=location)
        logger.info(f"zora_messages: location {location} added to key: {key}")
    return __format_message(message, *args, **kwargs)


def __format_message(message, *args, **kwargs):
    message.value = message.value.format(*args, **kwargs)
    message.detailed = message.detailed.format(*args, **kwargs)
    return message


def _get_location():
    # looks in stack for the first call outside this file
    try:
        stack = next(st for st in inspect.stack()
                     if __file__ not in st.filename)
        filename = stack.filename.replace(settings.BASE_DIR, '')
        line = stack.lineno
        function = stack.function
        return f"{filename}:{line} in {function}"
    except StopIteration:             # pragma: no cover
        return ""

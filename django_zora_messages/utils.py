import logging
import inspect
from django_zora_messages.models import Message, MessageLocation
from functools import lru_cache
from django.conf import settings
from django.utils import translation

logger = logging.getLogger(__name__)

def _get_location():
    ## looks in stack for the first call outside this file 
    try:
        stack = next(st for st in inspect.stack() 
                    if not __file__ in st.filename)
        filename = stack.filename.replace(settings.BASE_DIR, '')
        line = stack.lineno
        function = stack.function
        return f"{filename}:{line} in {function}"
    except StopIteration:
        return ""


def get_message(key, language=None):
    if not language:
        language = translation.get_language()
    return __get_message(key, language)


@lru_cache(maxsize=3000)
def __get_message(key, language):
    
    if settings.DEBUG:    
        return __get_or_create_message(key, language)
    else:
        try:
            #this is the ideal behavior
            message = Message.objects.get(key=key, language=language)
        except Message.DoesNotExist:
            logger.error (f"zora_messages: key %s not found for language %s",
                          key, language)
            ## looks for a similar language in database
            ## example: when pt-br is not found, looks for pt
            if '-' in language:
                try:
                    lang2 = language[0:language.find('-')]
                    message = Message.objects.get(key=key, language=lang2)
                    logger.warning(
                        f"using language %s instead of %s for key %s ",
                        lang2, language, key)
                except Message.DoesNotExist:
                    message = __empty_message(key, language)
            else:
                message = __empty_message(key, language)
    return message


def __empty_message(key, language):
    """ used in production to avoid the system to be aborted """
    return Message(key=key, value=key, language=language, 
                   detailed=key)


def __get_or_create_message(key, language):
    """ used in development to create a new message """
    
    message, new = Message.objects.get_or_create(key=key, language=language)

    if new:
        logger.info(f"zora_messages:Created a new message for key: {key}")
    location = _get_location()
    
    if not location in message.locations:
        MessageLocation.objects.create(key=key, location=location)
        logger.info(f"zora_messages: location {location} added to key: {key}")
    return message




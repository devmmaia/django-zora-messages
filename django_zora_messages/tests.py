
from django.test import TestCase

from django_zora_messages.utils import get_message as msg
from django_zora_messages.models import Message
from django.conf import settings
from django.test.utils import override_settings
from unittest import skip
from django.utils import translation


class UtilModuleTests(TestCase):

    @override_settings(DEBUG=True)
    def test_load_message_creates_a_new_message(self):
        message = msg("test.create.new.message")
        message2 = Message.objects.get(key="test.create.new.message")
        self.assertEquals(message, message2)


    @override_settings(DEBUG=True)
    def test_location_created_is_ok(self):
        expected = __file__.replace(settings.BASE_DIR, "")
        message = msg("test.location")
        self.assertTrue(expected in message.locations[0])


    @override_settings(DEBUG=False)
    def test_production_uses_similar_language(self):
        message = Message.objects.create(key="test.similar", language="pt")
        message2 = msg("test.similar", language_="pt-br")
        self.assertEquals(message.id, message2.id)


    @override_settings(DEBUG=False)
    def test_production_uses_empty_message(self):
        key = "test.unknown.key"
        message = msg(key)
        self.assertEquals(key, message.value)

    @override_settings(DEBUG=True)
    def test_format_value_args(self):
        val = "Este eh o teste numero {} chamado {}"
        expected = val.format(1, "test_format_args")

        Message.objects.create(key="tst.format.args", 
                               value=val, detailed=val, 
                               language=translation.get_language())

        message = msg("tst.format.args", 1, "test_format_args")
        self.assertEquals(expected, message.value)

    @override_settings(DEBUG=True)
    def test_format_value_kwargs(self):
        val = "Este eh o teste numero {num} chamado {test_name}"
        expected = val.format(num=1, test_name="test_format_kwargs")

        Message.objects.create(key="tst.format.args",
                               value=val, detailed=val,
                               language=translation.get_language())

        message = msg("tst.format.args", num=1, test_name="test_format_kwargs")
        self.assertEquals(expected, message.value)

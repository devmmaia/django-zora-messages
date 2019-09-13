
from django.db import models


class Message(models.Model):
    """ Describes every available language a massage was translated """

    key = models.CharField(max_length=50)
    language = models.CharField(max_length=10)
    value = models.CharField(max_length=50)
    detailed = models.CharField(max_length=1000)
    dev_instructions = models.CharField(max_length=2000)

    @property
    def locations(self):
        return list({loc.location for loc in 
                    MessageLocation.objects.filter(key=self.key)})

    def __str__(self):
        return self.value

    class Meta:
        unique_together = ('key', 'language',)


class MessageLocation(models.Model):
    """ Describes the Files and lines where this message was used """
    key = models.CharField(max_length=50)
    location = models.CharField(max_length=100)

    class Meta:
        unique_together = ('key', 'location',)

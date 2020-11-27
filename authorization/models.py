from django.db import models
from apis.models import App
from ml.models import Images


class User(models.Model):
    open_id = models.CharField(max_length=32, unique=True)
    nickname = models.CharField(max_length=256)
    focus_cities = models.TextField(default='[]')
    focus_cropIds = models.TextField(default='[]')
    menu = models.ManyToManyField(App)
    image = models.ManyToManyField(Images)



    class Meta:
        indexes = [
            models.Index(fields=['nickname']),
            models.Index(fields=['open_id', 'nickname'])
        ]

    def __str__(self):
        return '%s' % (self.nickname)
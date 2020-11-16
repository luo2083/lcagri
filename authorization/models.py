from django.db import models
from apis.models import App


class User(models.Model):
    open_id = models.CharField(max_length=32, unique=True)
    nickname = models.CharField(max_length=256)
    focus_cities = models.TextField(default='[]')
    focus_constellations = models.TextField(default='[]')

    menu = models.ManyToManyField(App)



    class Meta:
        indexes = [
            models.Index(fields=['nickname']),
            models.Index(fields=['open_id', 'nickname'])
        ]

        def __str__(self):
            return '%s' % (self.nickname)
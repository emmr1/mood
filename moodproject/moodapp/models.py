from django.db import models
from django.conf import settings
from django.utils.timezone import now
import datetime

class UserStatistics(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    longest_streak = models.PositiveSmallIntegerField()

MOODS = [
    ('h', 'Happy'),
    ('s', 'Sad'),
    ('c', 'Calm'),
    ('a', 'Angry'),
 ]
class UserMood(models.Model):
    mood = models.CharField(max_length=1, choices=MOODS)
    created = models.DateTimeField(default=datetime.datetime.now) #default=now #auto_now_add=True
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    streak = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['created']

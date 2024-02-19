# checkins/models.py

from django.db import models
from django.contrib.auth.models import User

class CheckIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hours = models.FloatField()
    tag = models.CharField(max_length=100)
    activities = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'checkins'  # Define the app_label
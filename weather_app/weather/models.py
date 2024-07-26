
from django.db import models


class SearchHistory(models.Model):
    session_id = models.CharField(max_length=32)
    city = models.CharField(max_length=111)
    date_time = models.DateTimeField(auto_now_add=True)
    condition = models.CharField(max_length=100)
    temperature = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date_time']

    def __str__(self):
        return f'{self.city} ({self.date_time})'

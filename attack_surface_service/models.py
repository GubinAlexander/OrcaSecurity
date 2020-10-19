from django.db import models


class Statistic(models.Model):
    request_count = models.IntegerField(default=0)
    average_request_time = models.FloatField(default=0)

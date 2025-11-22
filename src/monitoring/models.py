from django.db import models

from django.db import models

class MonitorResult(models.Model):
    url = models.URLField(verbose_name="Website URL")
    status = models.IntegerField(default=200, verbose_name="HTTP Status")
    response_time = models.FloatField(verbose_name="Response Time (s)")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Check Time")
    is_up = models.BooleanField(default=True, verbose_name="Site Available")

    def __str__(self):
        return f"{self.url} - {self.status} ({self.timestamp})"


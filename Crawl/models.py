from django.db import models
from django.utils.translation import gettext_lazy as _
from jsonfield import JSONField

class ScrapedData(models.Model):
    data = models.JSONField()
    
    def __str__(self):
        return str(self.data)
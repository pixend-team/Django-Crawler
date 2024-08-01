from django.db import models
from django.utils.translation import gettext_lazy as _
from jsonfield import JSONField
from django.contrib.auth.models import User

class ScrapedData(models.Model):
    data = models.JSONField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.data)
    

from django.db import models

# Create your models here.

class TheodoTeam(models.Model):
    name = models.CharField(max_length=100000)
    image = models.CharField(max_length=150)
    fun_fact = models.TextField(blank=True)

    class Meta:
        verbose_name = "theodo UK team"
      
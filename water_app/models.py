from django.db import models

# Create your models here.
class WaterData(models.Model):
    datetime = models.DateTimeField()
    status_type = models.CharField(max_length=100)
    quality = models.CharField(max_length=100)


    def __str__(self):
      return f"Water Data - ID: {self.id}"
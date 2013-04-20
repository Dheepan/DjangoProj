from django.db import models

# Create your models here.

class Images(models.Model):
    image_id=models.CharField(max_length=200)
    coordinates=models.CharField(max_length=200)
    proc_time= models.DateTimeField('last processed timestamp')



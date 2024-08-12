from django.db import models

# Create your models here.

class itemModel(models.Model):
    itemId = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 50, unique=True)
    description = models.TextField()
    price = models.FloatField()
    # picture = models.ImageField()  not yet sure how to implement this


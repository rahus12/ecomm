from django.db import models
from login.models import UserModel
from item.models import ItemModel


# Create your models here.
class CartModel(models.Model):
    userId = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    itemId = models.ForeignKey(ItemModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()

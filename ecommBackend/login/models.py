from django.db import models
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.

# creating users
class UserModel(models.Model):
    userID = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=80, unique=True)
    password = models.CharField(max_length=80)



    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def verify_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.userName



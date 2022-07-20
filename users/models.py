from django.db import models

class User(models.Model):
    name          = models.CharField(max_length=50)
    username      = models.CharField(max_length=50, unique=True)
    password      = models.CharField(max_length=250)
    mobile_number = models.CharField(max_length=200)
    birth_day     = models.DateField()
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
from django.db   import models

from core.models import TimeStampModel

class User(TimeStampModel):
    name          = models.CharField(max_length=50)
    username      = models.CharField(max_length=50, unique=True)
    password      = models.CharField(max_length=250)
    mobile_number = models.CharField(max_length=200)
    birth_day     = models.DateField()

    class Meta:
        db_table = 'users'
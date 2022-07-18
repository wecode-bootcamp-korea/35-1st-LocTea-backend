from django.db import models

from categories.models import SecondCategory

class Product(models.Model):
    title = models.CharField(max_length=45)
    description = models.TextField()
    second_category = models.ForeignKey(SecondCategory, on_delete=models.CASCADE)
    price = models.IntegerField()
    stock = models.IntegerField()

    class Meta:
        db_table = 'products'
from django.db import models

class FirstCategory(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        db_table = 'first_categories'

class SecondCategory(models.Model):
    title = models.CharField(max_length=50)
    first_category = models.ForeignKey(FirstCategory, on_delete=models.CASCADE, related_name='second_categories')

    class Meta:
        db_table = 'second_categories'
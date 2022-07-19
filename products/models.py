from django.db          import models

from categories.models  import SecondCategory
from core.models        import TimeStampModel

class Product(TimeStampModel):
    title           = models.CharField(max_length=45)
    description     = models.TextField()
    second_category = models.ForeignKey(SecondCategory, on_delete=models.CASCADE)
    price           = models.DecimalField()
    stock           = models.IntegerField()
    discount        = models.DecimalField(null=True)

    class Meta:
        db_table = 'products'
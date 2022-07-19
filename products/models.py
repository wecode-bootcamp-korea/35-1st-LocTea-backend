from django.db          import models

from categories.models  import SecondCategory
from core.models        import TimeStampModel

class Type(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'types'

class Product(TimeStampModel):
    title           = models.CharField(max_length=45)
    description     = models.TextField()
    second_category = models.ForeignKey(SecondCategory, on_delete=models.CASCADE)
    price           = models.DecimalField(decimal_places=3, max_digits=10)
    stock           = models.IntegerField()
    discount        = models.DecimalField(null=True, decimal_places=0, max_digits=3)
    type            = models.ManyToManyField('Type')

    class Meta:
        db_table = 'products'

class Thumbnail_image(models.Model):
    url     = models.URLField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='thumbnail_images')
    
    class Meta:
        db_table = 'thumbnail_images'

class Detail_image(models.Model):
    url     = models.URLField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='detail_images')
    
    class Meta:
        db_table = 'detail_images'





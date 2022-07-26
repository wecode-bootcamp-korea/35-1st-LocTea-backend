from django.db       import models

class Cart(models.Model) :
    user     = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True)
    product  = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    
    class Meta :
        db_table = 'carts'

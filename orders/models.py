from django.db   import models

from core.models import TimeStampModel
    
class Order(TimeStampModel) :
    user         = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product      = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    order_status = models.ForeignKey('OrdersStatus', on_delete=models.CASCADE)

    class Meta :
       db_table = 'orders'


class OrderStatus(models.Model) :
    status = models.CharField(max_length=200)

    class Meta :
       db_table = 'orders_status'

class OrderItem(models.Model) :
    order              = models.ForeignKey('Order', on_delete=models.CASCADE)
    product            = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity           = models.IntegerField()
    order_items_status = models.ForeignKey('OrderItemsStatus', on_delete=models.CASCADE)

    class Meta :
       db_table = 'order_items'

class OrderItemStatus(models.Model) :
    status = models.CharField(max_length=200)

    class Meta :
       db_table = 'order_items_status'
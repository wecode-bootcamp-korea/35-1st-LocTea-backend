import json

from django.views    import View
from django.http     import JsonResponse

from cart.models            import Cart
from users.models           import User
from products.models        import Product
from orders.models          import Order, OrderStatus, OrderItem, OrderItemStatus
from core.utils             import login_decorator

class OrderView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)    
            product_id = data["product_id"]
            user = data["user.id"]      
            order = data["order"]

            
            if Cart.quantity < 1 or Cart.quantity > Product.stock :
                return JsonResponse({"message" : "INVALID_QUANTITY"}, status=400)

            Order.objects.create(
                user            = request.user.id,
                stock           = order.product.stock,
                order_number    = order.id,
                order_status_id = 

    
        
        

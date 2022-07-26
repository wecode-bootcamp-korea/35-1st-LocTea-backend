import json

from django.views    import View
from django.http     import JsonResponse
from json.decoder    import JSONDecodeError

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
            order = data["order"]
            
            Order.objects.create(
                user         = request.user,
                product_id   = product_id,
                order_status = order['status'],
                address      = order['address'],
            )
            
            return JsonResponse({'message': 'SUCCESS'}, status=200)
        
        except JSONDecodeError :
            return JsonResponse({'message': "JSON_DECODE_ERROR"}, status=400)
        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

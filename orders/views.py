import json

from django.views    import View
from django.http     import JsonResponse
from json.decoder    import JSONDecodeError
from django.db       import transaction

from cart.models            import Cart
from users.models           import User
from products.models        import Product
from orders.models          import Delivery, Order, OrderStatus, OrderItem, OrderItemStatus
from core.utils             import login_decorator
from core.enums             import OrderStatusEnum

class OrderView(View):
    @login_decorator
    @transaction.atomic
    def post(self, request):
        try:
            data              = json.loads(request.body)
            user              = request.user
            order_id          = data['order_id']
            address           = data['address']
            recipient         = data['recipient']
            recipient_contact = data['recipient_contact']
            sender            = data['sender']
            cart_id           = data['cart_id']
            
            order_status      = OrderStatus.objects.get(id=OrderStatusEnum.COMPLETED.value)
            cart              = Cart.objects.get(id=cart_id)
        
            Order.objects.create(
                user         = user,
                product_id   = cart.product_id,
                order_status = order_status,
                )
            Delivery.objects.create(
                address           = address,
                sender            = sender,
                recipient         = recipient,
                recipient_contact = recipient_contact,
                order_id          = order_id
                )   
            cart.delete()
            
            return JsonResponse({'message': 'SUCCESS'}, status=200)
        
        except Cart.DoesNotExist :
            return JsonResponse({'message': "Cart.DoesNotExist"}, status=400)    
        except JSONDecodeError :
            return JsonResponse({'message': "JSON_DECODE_ERROR"}, status=400)
        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
    
    @login_decorator
    def get(self , request):

        orders = Order.objects.filter(user=request.user)

        result = [{
            'order_id'         : order.id,
               
        } for order in orders]
 
        return JsonResponse({"result":result}, status = 200)
        
        
        
import json

from django.views    import View
from django.http     import JsonResponse

from orders.models   import Order, OrderStatus, OrderItem, OrderItemStatus
from core.utils      import login_decorator

class OrderView(View):
    @login_decorator
    def post(self, request):
        data  = json.loads(request.body)
        user = request.user
        

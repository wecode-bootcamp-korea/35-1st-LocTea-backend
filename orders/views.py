import json

from django.views    import View
from django.http     import JsonResponse

from orders.models   import Order, OrderStatus, OrderItem, OrderItemStatus
from core.utils      import LoginDecorator

class OrderView(View):
    @LoginDecorator
    def post(self, request):
        data  = json.loads(request.body)
        user = request.user
        

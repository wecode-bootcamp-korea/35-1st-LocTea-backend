import json
from json.decoder           import JSONDecodeError

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import MultipleObjectsReturned

from cart.models            import Cart
from users.models           import User
from products.models        import Product
from core.utils             import LoginDecorator

class CartView(View) :
    @LoginDecorator
    def post(self, request) :
        try :
            data       = json.loads(request.body)
            user       = request.user
            product_id = data['product_id']
            quantity   = data['quantity']

            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'message':'PRODUCT_NOT_EXIST'}, status=400)

            if quantity <= 0:
                return JsonResponse({'message':'QUANTITY_ERROR'}, status=400)
        
            cart, is_created  = Cart.objects.get_or_create(
                user_id       = user.id,
                product_id    = product_id
            )
            cart.quantity += quantity
            cart.save()
            
            if is_created == 0 :
                return JsonResponse({'message': 'UPDATE_SUCCESS'}, status=200)
            return JsonResponse({'message': 'CREATE_SUCCESS'}, status=201)
            
        except Cart.DoesNotExist :
            return JSONDecodeError({'message':'INVAILD_CART'}, status=400)
        except JSONDecodeError :
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        except KeyError :
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

    @LoginDecorator
    def get(self, request):
        user  = request.user.id
        carts = Cart.objects.filter(user_id=user)
        
        result = [{
            'username'        : user,
            'cart_id'         : cart.id,
            'product_id'      : cart.product.id,
            'title'           : cart.product.title,
            'quantity'        : cart.quantity,
            'price'           : cart.product.price,
            'thumbnail_images': cart.product.thumbnail_images.first(),
            'discount'        : cart.product.discount,
            'stock'           : cart.product.stock

        } for cart in carts]

        return JsonResponse({"result":result}, status = 200)
    
    @LoginDecorator
    def delete(self, request):
        try:    
            data    = json.loads(request.body)
            user    = request.user
            cart_id = data['cart_id']
            cart    = Cart.objects.get(id=cart_id, user=user)

            cart.delete()
            return JsonResponse({'message':'DELETED'}, status=200)

        except MultipleObjectsReturned :
            return JsonResponse({'message':'MULTIPLE_OBJECTS_RETURNED'}, status=400)
        except ValueError :
            return JsonResponse({'message':'VAULE_ERROR'}, status=400)

    @LoginDecorator
    def patch(self, request) :
        try :
            data     = json.loads(request.body)
            user     = request.user.id
            cart_id  = data['cart_id']
            quantity = data['quantity']
           
            if quantity <= 0:
                return JSONDecodeError({'message':'QUANTITY_ERROR'}, status=400)

            cart = Cart.objects.get(id=cart_id, user=user)

            cart.quantity = data['quantity']
            cart.save()
            return JsonResponse({'quantity':cart.quantity}, status=200)

        except MultipleObjectsReturned:
            return JsonResponse({'message':'MULTIPLE_OBJECT_RETURNED'}, status=400)
        except JSONDecodeError :
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)   